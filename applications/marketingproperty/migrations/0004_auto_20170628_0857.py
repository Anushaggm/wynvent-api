# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketingproperty', '0003_auto_20170628_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='Propertydetails',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('property_type', models.CharField(blank=True, max_length=255, null=True)),
                ('property_subtype', models.CharField(blank=True, max_length=255, null=True)),
                ('seller_type', models.CharField(blank=True, max_length=255, null=True)),
                ('ownership', models.CharField(blank=True, max_length=255, null=True)),
                ('property_area', models.CharField(blank=True, max_length=255, null=True)),
                ('property_land_area', models.CharField(blank=True, max_length=255, null=True)),
                ('property_carpet_area', models.CharField(blank=True, max_length=255, null=True)),
                ('total_price', models.CharField(blank=True, max_length=255, null=True)),
                ('other_charges', models.CharField(blank=True, max_length=255, null=True)),
                ('all_inclusive_price', models.CharField(blank=True, max_length=255, null=True)),
                ('transaction_type', models.CharField(blank=True, max_length=255, null=True)),
                ('current_status', models.CharField(blank=True, max_length=255, null=True)),
                ('possession', models.CharField(blank=True, max_length=255, null=True)),
                ('construction_age', models.CharField(blank=True, max_length=255, null=True)),
                ('pre_leased', models.CharField(blank=True, max_length=255, null=True)),
                ('locality', models.CharField(blank=True, max_length=255, null=True)),
                ('full_address', models.CharField(blank=True, max_length=500, null=True)),
                ('project_name', models.CharField(blank=True, max_length=255, null=True)),
                ('floor', models.CharField(blank=True, max_length=255, null=True)),
                ('property_total_floors', models.CharField(blank=True, max_length=255, null=True)),
                ('property_towers', models.CharField(blank=True, max_length=255, null=True)),
                ('property_units', models.CharField(blank=True, max_length=255, null=True)),
                ('number_of_lifts', models.CharField(blank=True, max_length=255, null=True)),
                ('bedroom', models.CharField(blank=True, max_length=255, null=True)),
                ('bathroom', models.CharField(blank=True, max_length=255, null=True)),
                ('pooja_room', models.CharField(blank=True, max_length=255, null=True)),
                ('study_room', models.CharField(blank=True, max_length=255, null=True)),
                ('servant_room', models.CharField(blank=True, max_length=255, null=True)),
                ('balcony', models.CharField(blank=True, max_length=255, null=True)),
                ('flooring', models.CharField(blank=True, max_length=255, null=True)),
                ('furnishing', models.CharField(blank=True, max_length=255, null=True)),
                ('pantry', models.CharField(blank=True, max_length=255, null=True)),
                ('maintenance_charge', models.CharField(blank=True, max_length=255, null=True)),
                ('maintenance_charge_type', models.CharField(blank=True, max_length=255, null=True)),
                ('overlooking', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_loan', models.CharField(blank=True, max_length=255, null=True)),
                ('amenities', models.CharField(blank=True, max_length=1000, null=True)),
                ('landmarks', models.CharField(blank=True, max_length=255, null=True)),
                ('car_park', models.CharField(blank=True, max_length=255, null=True)),
                ('builder', models.CharField(blank=True, max_length=255, null=True)),
                ('agent_details', models.CharField(blank=True, max_length=2000, null=True)),
                ('project_details', models.CharField(blank=True, max_length=255, null=True)),
                ('width_road_facing', models.CharField(blank=True, max_length=255, null=True)),
                ('no_of_open_sides', models.CharField(blank=True, max_length=255, null=True)),
                ('boundary_wall', models.CharField(blank=True, max_length=255, null=True)),
                ('power_backup', models.CharField(blank=True, max_length=255, null=True)),
                ('gated_community', models.CharField(blank=True, max_length=255, null=True)),
                ('length', models.CharField(blank=True, max_length=255, null=True)),
                ('breadth', models.CharField(blank=True, max_length=255, null=True)),
                ('cabins', models.CharField(blank=True, max_length=255, null=True)),
                ('seats', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'propertydetails',
            },
        ),
        migrations.DeleteModel(
            name='MarketingProperty',
        ),
    ]
