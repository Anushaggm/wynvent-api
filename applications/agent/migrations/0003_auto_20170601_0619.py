# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 06:19
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_auto_20170530_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='founded_date',
            field=models.DateField(blank=True, null=True, verbose_name='Operating Since'),
        ),
    ]