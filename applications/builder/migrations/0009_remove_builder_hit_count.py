# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-31 19:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0008_auto_20170731_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builder',
            name='hit_count',
        ),
    ]
