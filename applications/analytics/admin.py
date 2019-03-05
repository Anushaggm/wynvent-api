# coding=utf-8

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from applications.analytics.models import LogStashConfiguration

admin.site.register(LogStashConfiguration, SingletonModelAdmin)
