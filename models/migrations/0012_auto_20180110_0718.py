# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_eventdetails_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='phone',
            field=models.CharField(default=None, max_length=20, unique=True),
        ),
    ]
