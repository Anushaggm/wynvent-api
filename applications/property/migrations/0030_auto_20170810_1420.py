# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-10 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0029_propertyanalytics'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyanalytics',
            options={'ordering': ['-created'], 'verbose_name': 'Property Analytics', 'verbose_name_plural': 'Property Analytics'},
        ),
        migrations.AddField(
            model_name='propertyanalytics',
            name='month',
            field=models.PositiveIntegerField(default=0, verbose_name='Month'),
        ),
        migrations.AddField(
            model_name='propertyanalytics',
            name='year',
            field=models.PositiveIntegerField(default=0, verbose_name='Year'),
        ),
    ]
