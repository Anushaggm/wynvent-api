from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db.models import PointField

from utils.db import WynventPostgresDBBaseModel


class City(WynventPostgresDBBaseModel):

    """ Model to store cities """

    name = models.CharField(max_length=255)
    coordinates = PointField(null=True)

    class Meta:
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name


class Locality(WynventPostgresDBBaseModel):

    """
    Data model to store localities within a city.
    """

    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, null=True)
    coordinates = PointField(null=True)

    class Meta:
        verbose_name_plural = _('Localities')

    def __str__(self):
        return '%s, %s' % (self.name, self.city)
