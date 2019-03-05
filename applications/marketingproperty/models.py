from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Propertydetails(models.Model):
    """
    To import properties from external DB.
    """

    property_id = models.IntegerField(primary_key=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    property_subtype = models.CharField(max_length=255, blank=True, null=True)
    seller_type = models.CharField(max_length=255, blank=True, null=True)
    # ownership = models.CharField(max_length=255, blank=True, null=True)
    # property_area = models.CharField(max_length=255, blank=True, null=True)
    property_land_area = models.CharField(max_length=255, blank=True, null=True)
    property_carpet_area = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.CharField(max_length=255, blank=True, null=True)
    other_charges = models.CharField(max_length=255, blank=True, null=True)
    all_inclusive_price = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    current_status = models.CharField(max_length=255, blank=True, null=True)#
    possession = models.CharField(max_length=255, blank=True, null=True)#
    construction_age = models.CharField(max_length=255, blank=True, null=True)
    pre_leased = models.CharField(max_length=255, blank=True, null=True)#
    city = models.CharField(max_length=255, blank=True, null=True)#
    locality = models.CharField(max_length=255, blank=True, null=True)
    full_address = models.CharField(max_length=500, blank=True, null=True)
    project_name = models.CharField(max_length=255)
    floor = models.CharField(max_length=255, blank=True, null=True)
    property_total_floors = models.CharField(max_length=255, blank=True, null=True)
    property_towers = models.CharField(max_length=255, blank=True, null=True)#
    property_units = models.CharField(max_length=255, blank=True, null=True)#
    number_of_lifts = models.CharField(max_length=255, blank=True, null=True)#
    bedroom = models.CharField(max_length=255, blank=True, null=True)
    bathroom = models.CharField(max_length=255, blank=True, null=True)#
    pooja_room = models.CharField(max_length=255, blank=True, null=True)#
    study_room = models.CharField(max_length=255, blank=True, null=True)#
    servant_room = models.CharField(max_length=255, blank=True, null=True)#
    balcony = models.CharField(max_length=255, blank=True, null=True)
    flooring = models.CharField(max_length=255, blank=True, null=True)
    furnishing = models.CharField(max_length=255, blank=True, null=True)#choice field
    pantry = models.CharField(max_length=255, blank=True, null=True)
    maintenance_charge = models.CharField(max_length=255, blank=True, null=True)#
    maintenance_charge_type = models.CharField(max_length=255, blank=True, null=True)#
    overlooking = models.CharField(max_length=255, blank=True, null=True)#
    bank_loan = models.CharField(max_length=255, blank=True, null=True)#
    amenities = models.CharField(max_length=1000, blank=True, null=True)#
    landmarks = models.CharField(max_length=255, blank=True, null=True)
    car_park = models.CharField(max_length=255, blank=True, null=True)
    # builder = models.CharField(max_length=255, blank=True, null=True)#
    agent_details = models.CharField(max_length=2000, blank=True, null=True)#
    project_details = models.CharField(max_length=255, blank=True, null=True)
    width_road_facing = models.CharField(max_length=255, blank=True, null=True)#
    no_of_open_sides = models.CharField(max_length=255, blank=True, null=True)
    boundary_wall = models.CharField(max_length=255, blank=True, null=True)#
    power_backup = models.CharField(max_length=255, blank=True, null=True)#
    gated_community = models.CharField(max_length=255, blank=True, null=True)#
    length = models.CharField(max_length=255, blank=True, null=True)
    breadth = models.CharField(max_length=255, blank=True, null=True)#
    cabins = models.CharField(max_length=255, blank=True, null=True)#
    seats = models.CharField(max_length=255, blank=True, null=True)#
    latitude = models.CharField(max_length=255, blank=True, null=True)#
    longitude = models.CharField(max_length=255, blank=True, null=True)#
    # exported = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = u'propertydetails'
        verbose_name = _('Property Details')
        verbose_name_plural = _('Property Details')

    def __str__(self):
        if  self.property_type:
            return self.property_type
        else:
            return self.property_type


class Images(models.Model):
    """
    To import property images from external DB.
    """
    property_id = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    property_id_website = models.CharField(max_length=255, blank=True, null=True)
    source_website = models.CharField(max_length=255, blank=True, null=True)
    image_url_s3 = models.CharField(max_length=255, blank=True, null=True)
    image_type = models.CharField(max_length=255, blank=True, null=True)
    s3_status = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    image_name_automated = models.CharField(max_length=255, blank=True, null=True)
    download_date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = u'images'
        verbose_name = _('Property Image')
        verbose_name_plural = _('Property Images')