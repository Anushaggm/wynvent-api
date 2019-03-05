# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-31 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0009_remove_builder_hit_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='builder',
            name='click_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Click Count'),
        ),
    ]