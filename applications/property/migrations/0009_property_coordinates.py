# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 12:58
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_auto_20170619_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
