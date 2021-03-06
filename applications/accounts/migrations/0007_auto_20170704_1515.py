# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-04 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_contactus_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agent.Agent'),
        ),
        migrations.AlterField(
            model_name='user',
            name='builder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builder.Builder'),
        ),
    ]
