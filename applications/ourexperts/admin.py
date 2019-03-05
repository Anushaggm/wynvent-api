from django.contrib import admin

from applications.ourexperts.models import OurExperts, ExpertResponses

admin.site.register(OurExperts)
admin.site.register(ExpertResponses)