# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20170601_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='available_from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='balcony_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='bathroom_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='bedroom_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='carpet_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='completeness_percent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='covered_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='expected_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='floor_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='monthly_rent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='no_of_open_sides',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='parking_count_four',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Four Wheeler Parking count'),
        ),
        migrations.AlterField(
            model_name='property',
            name='parking_count_two',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Two Wheeler Parking count'),
        ),
        migrations.AlterField(
            model_name='property',
            name='plot_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='plot_length',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='plot_width',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_per_sq_yard',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='security_deposit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='total_floor_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='washrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='width_of_road_facing_plot',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
