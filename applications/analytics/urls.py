# coding=utf-8

from django.conf.urls import url

from applications.analytics.views import LogStashDataView


urlpatterns = [
    url(r'^data/process/$', LogStashDataView.as_view(),name='log-stash-data-view'),
 ]