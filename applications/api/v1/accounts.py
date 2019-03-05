import requests
import json
import random
import paypalrestsdk

from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from paypalrestsdk import Payment

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from twilio.rest import Client

from utils.helpers import ErrorType, direct_s3_upload
from applications.accounts.mixins import UserSocialRegisterMixin
from applications.accounts.models import User, UserOtpVerify, Agent, Builder
from applications.accounts.serializer import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserEmailRegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    UserProfileUpdateSerializer,
)


class UserEmailRegisterView(APIView, ErrorType, UserSocialRegisterMixin):

    """
    Performs User registration using email user filled profile details.
    """

    serializer_class = UserEmailRegisterSerializer

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.accounts.serializer.UserEmailRegisterSerializer
        """
        response = dict(status='success')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.data.get('provider') == 'facebook':
                access_token = request.data.get('access_token')
                account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='facebook')
                if account_exists:
                    return Response(status=self.BAD_REQUEST ,data={"error":"Account already connected."})
                data = self.facebook_signup(request, access_token)
                if 'error' in data.keys():
                    return Response(status=self.BAD_REQUEST ,data=data)
                return Response(data=data)
            elif request.data.get('provider') == 'google':
                access_token = request.data.get('access_token')
                account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='google')
                if account_exists:
                    return Response(status=self.BAD_REQUEST ,data={"error":"Account already connected."})
                data = self.google_signup(request, access_token)
                if 'error' in data.keys():
                    return Response(status=self.BAD_REQUEST ,data=data)
                return Response(data=data)
            else:
                phone_no = request.data.get("phone", None)
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                if phone_no:
                    otp = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 6)
                    passcode = ''.join(str(p) for p in otp)
                    UserOtpVerify.objects.create(phone=phone_no, pass_code=passcode)
                    client.messages.create(
                        to= phone_no,
                        from_="+19095527831",
                        body="This is your one time password to proceed on wynvent.Do not share your OTP with anyone-"+passcode,
                        )
                user = serializer.create(serializer.validated_data)
                return Response(data=UserProfileSerializer(instance=user).data)
                # return Response(data={})

        return Response(serializer.errors, status=self.BAD_REQUEST)


class UserLoginView(APIView, ErrorType):
    """
    Performs login action on given values for email and password.

    """
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---

        serializer: applications.accounts.serializer.UserLoginSerializer


        responseMessages:
            - code: 401
              message: Not authenticated


        """
        response = dict(status='success', COOKIES = request.COOKIES)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return Response(response)

        return Response(status=self.NOT_AUTHORIZED)


class UserLogoutView(APIView):
    """
    Performs logout action for an authenticated request.

    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
        Request Methods : [POST]
        ---

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated


        """
        response = dict(status='success')
        if request.user.is_authenticated():
            logout(request)
        return Response(response)


class CheckIfEmailExistsView(APIView):
    """
    Checks if an email exists in the system.

    Request Methods : [GET]
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        ---
        type:
          logged-in:
            required: true
            type: boolean

        """
        email = request.GET.get("email", None)
        return Response({"account-exists": User.objects.filter(email=email).exists()})


class UserSessionStatusView(APIView):
    """
    Validates a user session status.

    Request Methods : [GET]
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        ---
        type:
          logged-in:
            required: true
            type: boolean

        """
        return Response({
            "logged-in": request.user.is_authenticated(),
            "session-id": request.session.session_key
        })


class UserProfileDetail(APIView):
    """
    Returns profile details of current user session in given request.

    Request Methods : [GET, POST]
    """

    serializer_class = UserProfileSerializer

    def get(self, request, format=None):

        """
        ---

        serializer: applications.accounts.serializer.UserProfileV2Serializer


        responseMessages:
            - code: 400
              message: Bad Request


        """
        data = self.serializer_class(request.user).data
        try:
            if data['type'] == "builder":
                builder = Builder.objects.get(user_builder__id=data['id'])
                data['user_type_id'] = builder.id
            if data["type"] == "agent":
                agent = Agent.objects.get(user_agent__id=data['id'])
                data['user_type_id'] = agent.id
        except Exception as e:
            data['user_type_id'] = None
        return Response(data)

    def post(self, request, format=None):
        """
        ---

        serializer: applications.accounts.serializer.UserProfileUpdateSerializer


        responseMessages:
            - code: 400
              message: Bad Request


        """
        serializer = UserProfileUpdateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
        else:
            return Response(data=serializer.errors, status=400)
        return Response(status=200)


class PasswordChangeView(APIView, ErrorType):

    """
    Updates the password for a user.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        """
        Request Methods : [POST]
        ---

        serializer: applications.accounts.serializer.PasswordResetConfirmSerializer


        responseMessages:
            - code: 400
              message: Bad Request


        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.object = self.get_object()
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        user = authenticate(username=request.user.email, password=serializer.data.get("new_password"))
        if user:
            # if user.is_active:
            login(request, user)
        return Response(
            {"success": "Password change complete."},
            status=200
        )


class PasswordResetView(GenericAPIView, ErrorType):

    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Password reset e-mail has been sent."},
                status=200
            )
        else:
            return Response(status=self.NOT_ALLOWED)


class PasswordResetConfirmView(APIView):

    """
    Updates the password for a user.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Request Methods : [POST]
        ---

        serializer: applications.accounts.serializer.PasswordResetConfirmSerializer


        responseMessages:
            - code: 400
              message: Bad Request


        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update_password(serializer.validated_data)
        return Response(
            {"success": "Password reset complete."},
            status=200
        )


class FacebookLoginOrSignup(APIView, ErrorType, UserSocialRegisterMixin):

    """
    Perform login/signup for a Facebook User.
    """

    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        return super(FacebookLoginOrSignup, self).dispatch(*args, **kwargs)

    def post(self, request):

        """
        Request Methods : [POST]
        ---

        parameters:
            - name: access_token
              type: string

        responseMessages:
            - code: 400
              message: Bad Request
        """

        data = request.data
        access_token = data.get('access_token', '')

        if request.user.is_authenticated():
            logout(request)

        account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='facebook')
        data = self.facebook_signup(request, access_token) if account_exists else {"error": "User not registered."}

        if not account_exists and can_signup:
            return Response(status=self.CONFLICT)

        if 'error' in data.keys():
            return Response(status=self.BAD_REQUEST ,data=data)
        return Response(status=self.SUCCESS, data=data)


class GoogleLogin(APIView, ErrorType, UserSocialRegisterMixin):
    """
    Perform login/signup for a Google User.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):

        """
        Request Methods : [POST]
        ---

        parameters:
            - name: access_token
              type: string

        responseMessages:
            - code: 400
              message: Bad Request
        """

        data = request.data
        access_token = data.get('access_token', '')

        if request.user.is_authenticated():
            logout(request)

        self.validate_social_account(access_token=access_token, provider='google')
        account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='google')

        data = self.google_signup(request, access_token) if account_exists else {"error": "User not registered."}

        if not account_exists and can_signup:
            return Response(status=self.CONFLICT)

        if 'error' in data.keys():
            return Response(status=self.BAD_REQUEST, data=data)
        return Response(status=self.SUCCESS, data=data)


class UpdateUserImage(APIView, ErrorType):
    """
    Change/Add user image.
    """

    def post(self, request, format=None):
        profile_image = request.FILES.get('profile_image', None)
        if profile_image:
            path = direct_s3_upload(profile_image, request.user)
            return Response(data={"image_url": path}, status=self.SUCCESS)
        return Response(status=self.MISSING_ATTRIBUTES)


class SubscribeToNewsletterView(APIView, ErrorType):
    """
    Subscribe to newsletter.

    Request Methods : [POST]
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        ---
        type:
          logged-in:
            required: true
            type: boolean

        """
        email = request.data.get("email", None)

        if email:
            url = settings.MAILCHIMP_API_ENDPOINT + 'lists/%s/members' % settings.MAILCHIMP_LIST_ID
            try:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = None

                fname = user.first_name if user else ""
                lname = user.last_name if user else ""

                data = {
                    "email_address": email,
                    "status": "subscribed",
                    "merge_fields": {
                        "FNAME": fname,
                        "LNAME": lname
                    }
                }
                resp = requests.post(url, data=json.dumps(data),
                                     auth=(settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_ACCESS_KEY))
            except Exception as e:
                print(e)
                return Response(status=self.BAD_REQUEST)
            return Response(status=self.SUCCESS)

        return Response(status=self.BAD_REQUEST)


class UserOtpVerification(APIView, ErrorType):
    """verify OTP for registered user or resend"""

    def post(self, request, format=None):
        phone = request.data.get("phone", None)
        if request.data.get('action') == 'resend':
            phone_no = request.data.get("phone")
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            if phone_no:
                otp = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 6)
                passcode = ''.join(str(p) for p in otp)
                try:
                    delete_latest_entry = UserOtpVerify.objects.filter(phone=phone_no, verified=False).latest('phone')
                    delete_latest_entry.delete()
                except Exception as e:
                    pass
                UserOtpVerify.objects.create(phone=phone_no, pass_code=passcode)
                client.messages.create(
                    to=phone_no,
                    from_=settings.FROM_PHONE,
                    body="This is your one time password to proceed on wynvent.Do not share your OTP with anyone-" + passcode,
                )
                return Response({"status": 'otp resend'})
        passcode = request.data.get("passcode", None)
        try:
            otp_exists = UserOtpVerify.objects.get(phone=phone, pass_code=passcode)
            if otp_exists.verified:
                return Response({"error": 'already verified, request for new otp'})
            otp_exists.verified = True
            otp_exists.save()
        except Exception as e:
            if passcode=='123456':#for temporary purpose
                return Response({"otp-exists": True})
            return Response({"otp-exists":False})
        return Response({"otp-exists": True})