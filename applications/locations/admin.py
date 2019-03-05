from django.contrib import admin

from mapwidgets.widgets import GooglePointFieldWidget

from applications.locations.models import *


class LocalityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(Locality, LocalityAdmin)
admin.site.register(City, LocalityAdmin)
