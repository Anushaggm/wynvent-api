# coding=utf-8

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from applications.general.models import SortConfiguration

admin.site.register(SortConfiguration, SingletonModelAdmin)
