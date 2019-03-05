from django.db import models
from django.contrib.gis.db.models import PointField
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django import forms

from utils.db import WynventPostgresDBBaseModel
from utils.constants import *


class Advertisement(WynventPostgresDBBaseModel):
    """
    model to add advertisements
    """
    image = models.ImageField(upload_to='advertisement', help_text="Accepted formats are .jpg, .png & .bmp of maximum size 2MB")
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title')
    url = models.URLField(blank=True)
    location = PointField(null=True, blank=True)

    # Analytics
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    click_count = models.PositiveIntegerField(_('Click Count'), default=0)
    response_count = models.PositiveIntegerField(_('Response Count'), default=0)

    class Meta:
        verbose_name_plural = _('Advertisements')

    def __str__(self):
        return self.title


def clean_image(value):
        image = value
        if image:
            from django.core.files.images import get_image_dimensions
            w, h = get_image_dimensions(image)
            if w != VALID_IMAGE_WIDTH or h != VALID_IMAGE_HEIGHT:
                raise forms.ValidationError(u'That image resolution is incorrect. The image needs to be ' + str(VALID_IMAGE_WIDTH) + 'px * ' + str(VALID_IMAGE_HEIGHT) + 'px.')
        return image


class Banner(WynventPostgresDBBaseModel):
    """
    model to add Banner
    """
    image = models.ImageField(upload_to='banner', help_text="Accepted formats are .jpg, .png & .bmp of maximum size 2MB",validators=[clean_image])
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    type = models.CharField(choices=BANNER_CHOICES, max_length=25)
    url = models.URLField(blank=True, help_text="If type is Property, provide url here")

    class Meta:
        verbose_name_plural = _('Banners')

    def __str__(self):
        return self.title


class ActivityBasedPopup(WynventPostgresDBBaseModel):
    """
    model to add Pdf and popup information
    """
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    file = models.FileField(upload_to='documents/')
    image = models.ImageField(upload_to='activity')
    for_new_user = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('Activity Based Popup')

    def __str__(self):
        return self.title


class UserTimerPopup(WynventPostgresDBBaseModel):
    """
    model to add popup information for professional help etc...
    """
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='timer')
    for_new_user = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('User Timer Popup')

    def __str__(self):
        return self.title