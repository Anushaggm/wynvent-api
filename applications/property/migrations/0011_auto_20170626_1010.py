# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_auto_20170626_0432'),
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