# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 07:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builder', '0005_auto_20170724_0701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builder',
            name='cities',
        ),
        migrations.AddField(
            model_name='builder',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='builder',
            name='user_builder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_builder', to=settings.AUTH_USER_MODEL),
        ),
    ]