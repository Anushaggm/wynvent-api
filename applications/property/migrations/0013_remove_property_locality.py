# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0012_auto_20170626_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='locality',
        ),
    ]