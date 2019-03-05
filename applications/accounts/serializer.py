# coding=utf-8

import datetime

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
# from haystack.query import SearchQuerySet

from applications.accounts import utils as account_utils
from applications.accounts.models import ContactUs, FeedBack

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):

    """
    Serializer for user login.
    Validates an email-password pair and authenticate it for login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    # password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
        else:
            raise serializers.ValidationError(_('Invalid credentials.'))

        attrs['user'] = user
        return attrs


class UserEmailRegisterSerializer(serializers.Serializer):

    """
    Serializer for user registration.
    Creates a user instance.
    """

    fname = serializers.CharField(required=False)
    lname = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False)
    provider = serializers.CharField(required=False, allow_blank=True)
    access_token = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ('fname','lname','phone','email','password','type','provider','access_token')

    def __init__(self, *args, **kwargs):
        super(UserEmailRegisterSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        has_provider = data.get('provider')
        password = data.get('password')
        email = data.get('email')
        if not has_provider:
            if not password or password == '':
                raise serializers.ValidationError(_('Password should not be empty.'))

            min_length = 8
            # At least one letter and one non-letter
            first_isalpha = password[0].isalpha()
            if len(password) < min_length or all(c.isalpha() == first_isalpha for c in password):
                raise serializers.ValidationError(_("Password must be at least %d characters long, "
                                                  "and contain one letter and one digit or special "
                                                  "character.") % min_length)

        try:
            User.objects.get(email=email)
            raise serializers.ValidationError(_('User with this email already exists.'))
        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        validated_data.update({
            'username':validated_data['email']
        })
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['fname'],
                                   last_name=validated_data['lname'],
                                   email=validated_data['email'],
                                   type=validated_data['type'],
                                   mobile=validated_data.get('phone',None))

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving user profile details.
    """

    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    about_me = serializers.SerializerMethodField()
    oauth = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'fname',
            'lname',
            'email',
            'phone',
            'about_me',
            'oauth',
            'image_url',
            'type'
        )

    def get_fname(self, obj):
        return '%s'%(obj.first_name)

    def get_lname(self, obj):
        return '%s'%(obj.last_name)

    def get_phone(self, obj):
        return '%s'%(obj.mobile) if obj.mobile else ''

    def get_about_me(self, obj):
        return '%s' % obj.about_me

    def get_oauth(self, obj):
        as_fb_user = SocialAccount.objects.filter(user_id= obj.id, provider='facebook')
        as_gp_user = SocialAccount.objects.filter(user_id= obj.id, provider='google')
        return {
            'facebook':as_fb_user.count() > 0,
            'google':as_gp_user.count() > 0
        }

    def get_image_url(self, obj):
        return obj.profile_image.url if obj.profile_image else ''


class UserProfileUpdateSerializer(serializers.Serializer):

    """
    Serializer for editing user profile details.
    """

    fname = serializers.CharField(required=False)
    lname = serializers.CharField(required=False, allow_blank=False)
    email = serializers.CharField()
    phone = serializers.CharField()
    property_for = serializers.CharField()
    about_me = serializers.CharField(required=False)
    password = serializers.CharField(required=False, allow_blank=True)

    def validate_password(self, value):
        request = self.context.get('request', None)
        password = value
        is_same_password = check_password(password, request.user.password)
        if is_same_password:
            raise serializers.ValidationError('You cannot use current password. Please try another.')
        return password

    def validate_email(self, value):
        request = self.context.get('request', None)
        if not value == request.user.email:
            try:
                User.objects.get(email=value)
                raise serializers.ValidationError('User with this email already exists.')
            except User.DoesNotExist:
                pass
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['fname']
        if validated_data.get('lname') is not None:
            instance.last_name = validated_data['lname']
        instance.email = validated_data['email']
        instance.mobile = validated_data['phone']
        instance.property_for = validated_data['property_for']
        instance.about_me = validated_data['about_me']
        password = validated_data.get('password')
        if validated_data.get('password'):
            instance.set_password(password)
        instance.save()


class PasswordChangeSerializer(serializers.Serializer):

    """
    Serializer for updating password of a user.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        request = self.context['request']
        password = value
        is_same_password = check_password(password, request.user.password)
        if not is_same_password:
            raise serializers.ValidationError('Please provide the correct password.')
        return password

    def validate_new_password(self, value):
        request = self.context['request']
        password = value
        is_same_password = check_password(password, request.user.password)
        if is_same_password:
            raise serializers.ValidationError('You cannot use current password. Please try another.')
        return password


class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """ Override this method to change default e-mail options
        """
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        user = User.objects.filter(username = value)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))
        if user.count() == 0:
            raise serializers.ValidationError(_("This email doesn't have any associated user account."))
        if user.count() == 1:
            if not user[0].has_usable_password(): raise serializers.ValidationError(_("User doesnot have a password or it may belongs to user registered via social method."))
        if user.count() > 1:
            raise serializers.ValidationError(_("Multiple users returned."))
        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'domain_override': settings.FRONTEND_HOST_URL,
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'html_email_template_name': 'registration/password_reset_email.html',
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):

    """
    Serializer for resetting password of a user with uid and token.
    """

    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = attrs
        user = None
        try:
            uid = force_text(urlsafe_base64_decode(data['uid']))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(_('Invalid uid.'))

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError(_('Invalid token.'))

        attrs.update(dict(user=user))
        return attrs

    def update_password(self, validated_data):
        user = validated_data['user']
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContactSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving contact details.
    """

    class Meta:
        model = ContactUs
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving feedback details.
    """

    class Meta:
        model = FeedBack
        fields = "__all__"