# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-07 09:01
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_locality_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
