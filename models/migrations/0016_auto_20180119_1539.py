# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0015_auto_20180116_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdetails',
            name='type',
            field=models.CharField(choices=[('event', 'event'), ('workshop', 'workshop'), ('gl', 'gl')], default='event', max_length=20),
        ),
    ]
