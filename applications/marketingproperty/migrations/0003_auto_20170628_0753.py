# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('marketingproperty', '0002_auto_20170628_0613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketingproperty',
            name='property_id',
        ),
        migrations.AddField(
            model_name='marketingproperty',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='balcony',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='bathroom',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='bedroom',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='car_park',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Four Wheeler Parking count'),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='construction_age',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='floor',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='flooring',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='full_address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='furnishing',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='length',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='locality',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='maintenance_charge',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='no_of_open_sides',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='pantry',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='pooja_room',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='project_details',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='project_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='property_carpet_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='property_total_floors',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='property_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='property_units',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='seller_type',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='study_room',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='marketingproperty',
            name='width_road_facing',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterModelTable(
            name='marketingproperty',
            table='propertydetails',
        ),
    ]
