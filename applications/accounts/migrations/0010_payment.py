# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 10:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_userotpverify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified at')),
                ('amount', models.PositiveIntegerField(blank=True, max_length=10, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=50, null=True)),
                ('expired', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_payment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
            },
        ),
    ]
