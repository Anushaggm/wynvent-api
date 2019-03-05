# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 07:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agent', '0004_agentresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='agent',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='logo',
            field=models.ImageField(blank=True, upload_to='builder/'),
        ),
        migrations.AddField(
            model_name='agent',
            name='project_handled',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='agent',
            name='user_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_agent', to=settings.AUTH_USER_MODEL),
        ),
    ]