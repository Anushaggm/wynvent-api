# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('blog', '0006_blogview'),
    ]

    operations = [
        migrations.AddField(
            model_name='talktoexpert',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.City'),
        ),
    ]
