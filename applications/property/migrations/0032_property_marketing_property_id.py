# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-28 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0031_auto_20170818_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='marketing_property_id',
            field=models.PositiveIntegerField(default=0, verbose_name='Marketing Propery Id'),
        ),
    ]
