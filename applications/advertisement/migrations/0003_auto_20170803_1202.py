# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-03 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_auto_20170731_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(help_text='Accepted formats are .jpg, .png & .bmp of maximum size 2MB', upload_to='advertisement'),
        ),
    ]
