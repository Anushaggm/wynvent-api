# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 11:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agent', '0003_auto_20170601_0619'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_type', models.CharField(choices=[('buyer_owner', 'Buyer/Owner'), ('agent', 'Agent'), ('builder', 'Builder')], default='buyer_owner', max_length=25)),
                ('name', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('message', models.TextField(blank=True)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_responses', to='agent.Agent')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='get_agent_responses', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_agent_responses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Agent Responses',
                'verbose_name': 'Agent Response',
            },
        ),
    ]
