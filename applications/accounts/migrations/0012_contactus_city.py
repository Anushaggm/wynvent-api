# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-16 05:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_city_coordinates'),
        ('accounts', '0011_auto_20170727_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.City'),
        ),
    ]
