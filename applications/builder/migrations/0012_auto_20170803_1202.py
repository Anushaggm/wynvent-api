# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-03 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0011_auto_20170803_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builder',
            name='property_type',
            field=models.ManyToManyField(blank=True, to='property.PropertyType'),
        ),
    ]