# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-05 06:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_talktoexpert_city'),
        ('zinnia', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='authors',
        ),
        migrations.AddField(
            model_name='entry',
            name='authors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='blog.BlogAuthor', verbose_name='author'),
        ),
    ]
