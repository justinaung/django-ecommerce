# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnpaidUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('last_notification', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
