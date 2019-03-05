from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField

from mapwidgets.widgets import GooglePointFieldWidget

from applications.property.models import *


class PropertyImagesInline(admin.TabularInline):
    model = PropertyImage


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_for', 'type', 'locality', 'created')
    list_filter = ('property_for', 'type', 'city', 'locality', 'expected_price', 'monthly_rent', 'total_price', 'security_deposit',)
    search_fields = ('name', )
    inlines = [PropertyImagesInline, ]
    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }


class PropertyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('property', 'created', 'view_count', 'click_count', 'response_count')
    list_filter = ('month', 'year', )

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyResponse)
admin.site.register(Facility)
admin.site.register(FacilityType)
admin.site.register(PropertyReport)
admin.site.register(PropertyType)
admin.site.register(PropertyAnalytics, PropertyAnalyticsAdmin)
