from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from applications.property.models import Property
from utils.db import WynventPostgresDBBaseModel


class Payment(WynventPostgresDBBaseModel):
    """
    model for payment details
    """

    payment_property = models.ForeignKey("payments.PropertyPayment", related_name="get_payment", null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    response = JSONField(default=False)

    class Meta:
        verbose_name = _('Payment')

    def __str__(self):
        return self.payment_id


class PropertyPayment(WynventPostgresDBBaseModel):
    """
    shows payment for each property
    """
    property = models.ForeignKey(Property, related_name="property_payments", null=True)
    billing_address = models.TextField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _('Property Payment')

    def __str__(self):
        return self.billing_address


class UserPayment(WynventPostgresDBBaseModel):
    """
    Payment for agent and builder
    """
    user = models.ForeignKey("accounts.User", related_name="user_payments", null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    response = JSONField(default=False)

    class Meta:
        verbose_name = _('User Payment')

    def __str__(self):
        return self.payment_id