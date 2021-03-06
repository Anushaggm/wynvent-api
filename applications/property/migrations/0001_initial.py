# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 18:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent', '0002_auto_20170530_1836'),
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builder', '0002_auto_20170530_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified at')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified at')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Facility Types',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified at')),
                ('property_for', models.CharField(choices=[('sale', 'Sale'), ('rent', 'Rent')], max_length=25)),
                ('name', models.TextField(blank=True, null=True, verbose_name='Property Name')),
                ('type', models.CharField(choices=[('residential_apartment_villa', 'Residential Apartment / Villa'), ('commercial_showroom_shop', 'Commercial Showroom / Shop')], max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=100)),
                ('building_name', models.CharField(blank=True, max_length=255)),
                ('bedroom_count', models.IntegerField(blank=True)),
                ('bathroom_count', models.IntegerField(blank=True)),
                ('balcony_count', models.IntegerField(blank=True)),
                ('parking_count_two', models.IntegerField(blank=True, verbose_name='Two Wheeler Parking count')),
                ('parking_count_four', models.IntegerField(blank=True, verbose_name='Four Wheeler Parking count')),
                ('furnished_status', models.BooleanField(default=False)),
                ('washrooms', models.IntegerField(blank=True)),
                ('covered_area', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('covered_area_unit', models.CharField(blank=True, choices=[('sq_ft', 'Sq-ft'), ('sq_yrd', 'Sq-yrd'), ('sq_m', 'Sq-m'), ('acre', 'Acre'), ('hectare', 'Hectare'), ('ground', 'Ground'), ('cent', 'Cent'), ('are', 'Are')], max_length=50)),
                ('main_road_facing', models.BooleanField(default=False)),
                ('personal_washroom', models.BooleanField(default=False)),
                ('corner_shop', models.BooleanField(default=False)),
                ('pantry', models.CharField(blank=True, choices=[('dry', 'Dry'), ('wet', 'Wet'), ('not_available', 'Not Available')], max_length=50)),
                ('total_floor_count', models.IntegerField(blank=True)),
                ('floor_number', models.IntegerField(blank=True)),
                ('no_of_open_sides', models.IntegerField(blank=True)),
                ('width_of_road_facing_plot', models.IntegerField(blank=True)),
                ('plot_area', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('plot_area_unit', models.CharField(blank=True, choices=[('sq_ft', 'Sq-ft'), ('sq_yrd', 'Sq-yrd'), ('sq_m', 'Sq-m'), ('acre', 'Acre'), ('hectare', 'Hectare'), ('ground', 'Ground'), ('cent', 'Cent'), ('are', 'Are')], max_length=50)),
                ('plot_length', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('plot_length_unit', models.CharField(blank=True, choices=[('ft', 'ft'), ('yrd', 'yrd'), ('m', 'm'), ('Acre', 'Acre'), ('Bigha', 'Bigha'), ('Hectare', 'Hectare'), ('Marla', 'Marla'), ('Kanal', 'Kanal'), ('Biswa1', 'Biswa1'), ('Biswa2', 'Biswa2'), ('Ground', 'Ground'), ('Aankadam', 'Aankadam'), ('Rood', 'Rood'), ('Chatak', 'Chatak'), ('Kottah', 'Kottah'), ('Marla', 'Marla'), ('Cent', 'Cent'), ('Perch', 'Perch'), ('Guntha', 'Guntha'), ('Are', 'Are')], max_length=50)),
                ('plot_width', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('plot_width_unit', models.CharField(blank=True, choices=[('ft', 'ft'), ('yrd', 'yrd'), ('m', 'm'), ('Acre', 'Acre'), ('Bigha', 'Bigha'), ('Hectare', 'Hectare'), ('Marla', 'Marla'), ('Kanal', 'Kanal'), ('Biswa1', 'Biswa1'), ('Biswa2', 'Biswa2'), ('Ground', 'Ground'), ('Aankadam', 'Aankadam'), ('Rood', 'Rood'), ('Chatak', 'Chatak'), ('Kottah', 'Kottah'), ('Marla', 'Marla'), ('Cent', 'Cent'), ('Perch', 'Perch'), ('Guntha', 'Guntha'), ('Are', 'Are')], max_length=50)),
                ('carpet_area', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('carpet_area_unit', models.CharField(blank=True, choices=[('sq_ft', 'Sq-ft'), ('sq_yrd', 'Sq-yrd'), ('sq_m', 'Sq-m'), ('acre', 'Acre'), ('hectare', 'Hectare'), ('ground', 'Ground'), ('cent', 'Cent'), ('are', 'Are')], max_length=50)),
                ('is_corner_plot', models.BooleanField(default=False)),
                ('available_from_date', models.DateField(blank=True)),
                ('available_immediately', models.BooleanField(default=False)),
                ('age_of_construction', models.CharField(blank=True, choices=[('new_construction', 'New Construction'), ('less_than_5_years', 'Less than 5 years'), ('5_to_10_years', '5 to 10 years'), ('10_to_15_years', '10 to 15 years'), ('15_to_20_years', '15 to 20 years'), ('above_20_years', 'Above 20 years')], max_length=100)),
                ('transaction_type', models.CharField(blank=True, choices=[('new_property', 'New Property'), ('resale', 'Resale')], max_length=50)),
                ('owners_residence', models.CharField(blank=True, choices=[('same_premise', 'Same premise'), ('away', 'Away')], max_length=50)),
                ('monthly_rent', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('maintenance_charges', models.BooleanField(default=False)),
                ('water_charges', models.BooleanField(default=False)),
                ('electricity_charges', models.BooleanField(default=False)),
                ('other_charges', models.CharField(blank=True, max_length=255)),
                ('security_deposit', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('price_per_sq_yard', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('expected_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('exclude_duty_and_reg_charges', models.BooleanField(default=False, verbose_name='Stamp duty and registration charges excluded')),
                ('rent_to_bachelors', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('does_not_matter', "Doesn't Matter")], max_length=50)),
                ('rent_to_family', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('does_not_matter', "Doesn't Matter")], max_length=50)),
                ('rent_to_non_vegetarians', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('does_not_matter', "Doesn't Matter")], max_length=50)),
                ('rent_to_with_pets', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('does_not_matter', "Doesn't Matter")], max_length=50)),
                ('interesting_details', models.TextField(blank=True)),
                ('landmarks_and_neighbourhood', models.TextField(blank=True)),
                ('video_link', models.URLField(blank=True)),
                ('completeness_percent', models.IntegerField(blank=True)),
                ('terms_agreed', models.BooleanField(default=False)),
                ('property_verified', models.BooleanField(default=False)),
                ('phone_verified', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_properties', to='agent.Agent')),
                ('builder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_properties', to='builder.Builder')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.City')),
                ('facilities', models.ManyToManyField(blank=True, to='property.Facility')),
                ('locality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Locality')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified at')),
                ('image', models.ImageField(upload_to='property/')),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_images', to='property.Property')),
            ],
            options={
                'verbose_name_plural': 'Property Images',
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='property.FacilityType'),
        ),
    ]
