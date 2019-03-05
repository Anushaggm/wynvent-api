# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from applications.accounts.models import *
from applications.accounts.forms import AdminUserChangeForm, AdminUserCreationForm


class UserModelAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (_('Profile'), {'fields': ('mobile', 'type', 'profile_image', 'about_me')}),
        (_('Other'), {'fields': ('builder', 'agent', 'shortlisted_properties')}),
    )

admin.site.register(User, UserModelAdmin)
admin.site.register(ContactUs)
admin.site.register(FeedBack)
admin.site.register(UserOtpVerify)