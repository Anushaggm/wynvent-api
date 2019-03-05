from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from utils.db import WynventPostgresDBBaseModel
from utils.constants import *
from multiselectfield import MultiSelectField

from applications.property.models import Property
from applications.locations.models import City


class Builder(WynventPostgresDBBaseModel):

    """ Builder model under a User  """
    user_builder = models.ForeignKey("accounts.User", related_name="get_builder", null=True)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="builder/", blank=True)
    property_type = models.ManyToManyField("property.PropertyType", blank=True)
    city = models.CharField(max_length=255, blank=True,)
    description = models.TextField(blank=True)

    featured = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    standard = models.BooleanField(default=False)
    payment_created = models.DateField(_('Payment Date'), null=True, blank=True)
    expired = models.BooleanField(_("Payment Expired"), default=False)

    verified = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='name')

    # Analytics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    click_count = models.PositiveIntegerField(_('Click Count'), default=0)
    response_count = models.PositiveIntegerField(_('Response Count'), default=0)

    def __str__(self):
        return self.name

