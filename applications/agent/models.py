from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from utils.db import WynventPostgresDBBaseModel
from utils.constants import *


class Agent(WynventPostgresDBBaseModel):

    """ Agent model under a User  """
    user_agent = models.ForeignKey("accounts.User", related_name="get_agent", null=True)
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="agent/", blank=True)
    property_type = models.ManyToManyField("property.PropertyType", blank=True)
    contact_person = models.CharField(blank=True, max_length=255)
    city = models.CharField(max_length=255, blank=True,)
    project_handled = models.CharField(max_length=255, blank=True,)
    founded_date = models.DateField(_("Operating Since"), null=True, blank=True)
    description = models.TextField(blank=True)

    featured = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    standard = models.BooleanField(default=False)
    payment_created = models.DateField(_('Payment Date'), null=True, blank=True)
    expired = models.BooleanField(_("Payment Expired"),default=False)

    verified = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='title')

    # Analytics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    click_count = models.PositiveIntegerField(_('Click Count'), default=0)
    response_count = models.PositiveIntegerField(_('Response Count'), default=0)

    def __str__(self):
        return self.title


class AgentResponse(models.Model):

    """ Agent Response model """
    timestamp = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=25, default=BUYER_OWNER)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), blank=True)
    message = models.TextField(blank=True)
    agent = models.ForeignKey(Agent, related_name="get_responses", null=True)
    owner = models.ForeignKey("accounts.User", related_name="get_agent_responses", null=True)
    user = models.ForeignKey("accounts.User", related_name="submitted_agent_responses", null=True)

    class Meta:
        verbose_name = _('Agent Response')
        verbose_name_plural = _('Agent Responses')

    def __str__(self):
        return "%s: %s" % (self.name, self.message)
