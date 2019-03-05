# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170530_1836'),
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shortlisted_properties',
            field=models.ManyToManyField(blank=True, related_name='shortlisted_properties', to='property.Property'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='accounts/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('buyer_owner', 'Buyer/Owner'), ('agent', 'Agent'), ('builder', 'Builder')], default='buyer_owner', max_length=25),
        ),
    ]