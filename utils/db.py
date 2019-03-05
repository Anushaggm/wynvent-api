# coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class WynventPostgresDBBaseModel(models.Model):

    """
    Base model for Postgresql DB.
    """

    created = CreationDateTimeField(_('Created at'))
    modified = ModificationDateTimeField(_('Modified at'))

    class Meta:
        abstract = True
