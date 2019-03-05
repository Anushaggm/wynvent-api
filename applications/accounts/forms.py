from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm


from applications.accounts.models import User


class AdminUserChangeForm(UserChangeForm):

    """
    AdminForm for updating an instance of custom USER_MODEL.
    """

    class Meta(UserChangeForm.Meta):
        model = User


class AdminUserCreationForm(UserCreationForm):

    """
    AdminForm for creating an instance of custom USER_MODEL.
    """

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
