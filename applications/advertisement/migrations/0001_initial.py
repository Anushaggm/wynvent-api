# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-31 06:54
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified at')),
                ('image', models.ImageField(upload_to='advertisement')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Advertisements',
            },
        ),
    ]
