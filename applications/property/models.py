from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.contrib.gis.db.models import PointField
from django.db.models.signals import post_delete, post_save, m2m_changed
from django.dispatch import receiver

from utils.db import WynventPostgresDBBaseModel
from applications.locations.models import City, Locality
from utils.helpers import get_new_property_image_path, send_user_property_activities, alert_by_sms
from utils.constants import *
# from utils.handlers import (
#     add_property_object_to_elastic_index,
#     generic_many_to_many_update_elastic,
#     delete_property_object_from_elastic_index
# )


class Property(WynventPostgresDBBaseModel):

    """ Property model  """

    # Relationships
    user = models.ForeignKey("accounts.User", related_name="get_properties", null=True)
    # builder = models.ForeignKey("builder.Builder", related_name="get_properties", null=True)
    # agent = models.ForeignKey("agent.Agent", related_name="get_properties", null=True)

    # Property Basic info
    property_for = models.CharField(choices=PROPERTY_FOR_CHOICES, max_length=25)
    name = models.TextField(_('Property Name'), null=True)
    type = models.CharField(choices=PROPERTY_TYPES, max_length=100)
    address = models.CharField(max_length=200)
    # locality = models.ForeignKey(Locality, null=True)
    locality = models.CharField(max_length=255, null=True)
    # city = models.ForeignKey(City, null=True)
    city = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=100)

    # Property Detail
    building_name = models.CharField(max_length=255, blank=True)
    bedroom_count = models.PositiveIntegerField(null=True, blank=True)
    bathroom_count = models.PositiveIntegerField(null=True, blank=True)
    balcony_count = models.PositiveIntegerField(null=True, blank=True)
    puja_room = models.BooleanField(default=False)
    study_room = models.BooleanField(default=False)
    store_room = models.BooleanField(default=False)
    parking_count_two = models.PositiveIntegerField(_('Two Wheeler Parking count'), null=True, blank=True)
    parking_count_four = models.PositiveIntegerField(_('Four Wheeler Parking count'), null=True, blank=True)
    furnished_status = models.CharField(choices=FURNISHED_STATUS_CHOICES, max_length=100, blank=True)
    washrooms = models.PositiveIntegerField(null=True, blank=True)
    main_road_facing = models.BooleanField(default=False)
    personal_washroom = models.BooleanField(default=False)
    corner_shop = models.BooleanField(default=False)
    pantry = models.CharField(choices=PANTRY_CHOICES, max_length=50, blank=True)
    facilities = models.ManyToManyField("Facility", blank=True)
    total_floor_count = models.PositiveIntegerField(null=True, blank=True)
    floor_number = models.PositiveIntegerField(null=True, blank=True)
    no_of_open_sides = models.PositiveIntegerField(null=True, blank=True)
    is_corner_plot = models.BooleanField(default=False)

    # Dimensions
    width_of_road_facing_plot = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    covered_area = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    covered_area_unit = models.CharField(choices=AREA_UNITS, max_length=50, blank=True)
    plot_area = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    plot_area_unit = models.CharField(choices=AREA_UNITS, max_length=50, blank=True)
    plot_length = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    plot_length_unit = models.CharField(choices=LENGTH_UNITS, max_length=50, blank=True)
    plot_width = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    plot_width_unit = models.CharField(choices=LENGTH_UNITS, max_length=50, blank=True)
    carpet_area = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    carpet_area_unit = models.CharField(choices=AREA_UNITS, max_length=50, blank=True)

    # Availability
    available_from_date = models.DateField(null=True, blank=True)
    available_immediately = models.BooleanField(default=False)
    age_of_construction = models.CharField(choices=CONSTRUCTION_AGE_CHOICES, max_length=100, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=50, blank=True)

    # Owner residence
    owners_residence = models.CharField(choices=OWNERS_RESIDENCE_TYPES, max_length=50, blank=True)

    # Financial Info
    monthly_rent = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    maintenance_charges = models.BooleanField(default=False)
    water_charges = models.BooleanField(default=False)
    electricity_charges = models.BooleanField(default=False)
    other_charges = models.CharField(max_length=255, blank=True)
    security_deposit = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    price_per_sq_yard = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    expected_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    exclude_duty_and_reg_charges = models.BooleanField(
        _("Stamp duty and registration charges excluded"), default=False)

    # Rent to tenants
    rent_to_bachelors = models.CharField(choices=TENANT_RENT_CHOICES, max_length=50, blank=True)
    rent_to_family = models.CharField(choices=TENANT_RENT_CHOICES, max_length=50, blank=True)
    rent_to_non_vegetarians = models.CharField(choices=TENANT_RENT_CHOICES, max_length=50, blank=True)
    rent_to_with_pets = models.CharField(choices=TENANT_RENT_CHOICES, max_length=50, blank=True)

    # Good to know
    interesting_details = models.TextField(blank=True)
    landmarks_and_neighbourhood = models.TextField(blank=True)

    # Media
    video_link = models.URLField(blank=True)

    # completeness_percent = models.PositiveIntegerField(null=True, blank=True)

    # Flags
    terms_agreed = models.BooleanField(default=False)
    property_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    is_premium = models.BooleanField(default=False)
    is_standard = models.BooleanField(default=False)
    payment_created_date = models.DateField(_('Payment Date'), null=True, blank=True)
    is_payment_expired = models.BooleanField(_("Payment Expired"),default=False)

    ongoing = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='name')
    coordinates = PointField(null=True)

    # Analytics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    click_count = models.PositiveIntegerField(_('Click Count'), default=0)
    response_count = models.PositiveIntegerField(_('Response Count'), default=0)

    marketing_property_id = models.PositiveIntegerField(_('Marketing Propery Id'), default=0)

    class Meta:
        verbose_name_plural = _('Properties')

    def __str__(self):
        return str(self.name)
# post_delete.connect(delete_property_object_from_elastic_index, sender=Property)
# post_save.connect(add_property_object_to_elastic_index, sender=Property)
# m2m_changed.connect(generic_many_to_many_update_elastic, sender=Property.facilities.through)

class Facility(WynventPostgresDBBaseModel):

    """ Facility model  """

    name = models.CharField(max_length=255)
    type = models.ForeignKey("FacilityType", related_name="facilities", null=True)

    class Meta:
        verbose_name_plural = _('Facilities')

    def __str__(self):
        return self.name


class FacilityType(WynventPostgresDBBaseModel):

    """ Facility type model  """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = _('Facility Types')

    def __str__(self):
        return self.name


class PropertyAnalytics(WynventPostgresDBBaseModel):
    """
    Data model for property analytics history
    """

    property = models.ForeignKey(Property, related_name="property_analytics")
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    click_count = models.PositiveIntegerField(_('Click Count'), default=0)
    response_count = models.PositiveIntegerField(_('Response Count'), default=0)
    month = models.PositiveIntegerField(_('Month'), default=0, choices=MONTHS)
    year = models.PositiveIntegerField(_('Year'), default=0)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Property Analytics')
        verbose_name_plural = _('Property Analytics')

    def __str__(self):
        return self.property.name


class PropertyImage(WynventPostgresDBBaseModel):

    """ Model to store images under a Property  """

    image = models.ImageField(upload_to=get_new_property_image_path)
    property = models.ForeignKey(Property, related_name="get_images", null=True)

    class Meta:
        verbose_name_plural = _('Property Images')

    def __str__(self):
        return self.property.name


class PropertyView(models.Model):
    datestamp = models.DateField(auto_now_add=True, null=True)
    property = models.ForeignKey(Property, related_name="get_views", null=True)

    class Meta:
        verbose_name = _('Property View')
        verbose_name_plural = _('Property Views')

    def __str__(self):
        return "%s : %s" % (self.timestamp, self.property.name)


class PropertyResponse(models.Model):

    """ Property Response model """
    timestamp = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=25, default=BUYER_OWNER)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), blank=True)
    message = models.TextField(blank=True)
    property = models.ForeignKey(Property, related_name="get_responses", null=True)
    owner = models.ForeignKey("accounts.User", related_name="get_property_responses", null=True)
    user = models.ForeignKey("accounts.User", related_name="submitted_property_responses", null=True)

    class Meta:
        verbose_name = _('Property Response')
        verbose_name_plural = _('Property Responses')

    def __str__(self):
        return "%s: %s" % (self.name, self.message)

@receiver(post_save, sender=PropertyResponse, dispatch_uid="post_save_contest_entry")
def contest_entry_signal(instance, **kwargs):
    created = kwargs['created']
    if created:
        message = 'A response has been generated from '+instance.email+' for the property '+instance.property.name
        alert_by_sms(instance.property.user.mobile, message)
        send_user_property_activities(instance.property.user, message)
    else:
        pass


class PropertyReport(models.Model):

    """ To Report Property """
    content = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), blank=True)
    property = models.ForeignKey(Property, related_name="get_reports", null=True)
    user = models.ForeignKey("accounts.User", related_name="property_reports", null=True)

    class Meta:
        verbose_name = _('Property Report')
        verbose_name_plural = _('Property Reports')

    def __str__(self):
        return "%s: %s" % (self.content, self.email)

class PropertyType(models.Model):

    """ Model for agent and builders property types """
    type = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Property Type')
        verbose_name_plural = _('Property Types')

    def __str__(self):
        return "%s" % (self.type)