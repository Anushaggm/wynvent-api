# coding=utf-8

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel

from utils.constants import SORT_OPTIONS


class SortConfiguration(SingletonModel):
    agent_sort = models.CharField(_('Agent Sort BY'), max_length=255, choices=SORT_OPTIONS, default="view_count")
    builder_sort = models.CharField(_('Builder Sort BY'), max_length=255, choices=SORT_OPTIONS, default="view_count")
    property_sort = models.CharField(_('Property Sort BY'), max_length=255, choices=SORT_OPTIONS, default="view_count")

    def __unicode__(self):
        return u"Sort Configuration"

    class Meta:
        verbose_name = _("Sort Configuration")