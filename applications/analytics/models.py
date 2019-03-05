# coding=utf-8

from django.db import models
from django.utils import timezone
from solo.models import SingletonModel


class LogStashConfiguration(SingletonModel):
    elastic_host = models.URLField(max_length=255, default="https://search-wynvent-staging-x24kbpqvt4mmhexwbbb3hhqn6q.us-west-2.es.amazonaws.com/")
    index = models.CharField(max_length=255, default="nginx-api-access")
    last_procesed = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"LogStash Configuration"

    class Meta:
        verbose_name = "LogStash Configuration"