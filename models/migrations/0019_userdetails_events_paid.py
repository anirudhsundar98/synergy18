# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-15 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0018_userdetails_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='events_paid',
            field=models.BooleanField(default=False),
        ),
    ]
