from django.contrib import admin
from django.contrib.gis.db.models import PointField
from django.db import models

from mapwidgets.widgets import GooglePointFieldWidget
from applications.advertisement.models import Advertisement, Banner, ActivityBasedPopup, UserTimerPopup


class AdvertisementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Banner)
admin.site.register(ActivityBasedPopup)
admin.site.register(UserTimerPopup)