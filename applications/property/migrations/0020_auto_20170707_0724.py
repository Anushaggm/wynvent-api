# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0019_remove_property_completeness_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='locality',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
