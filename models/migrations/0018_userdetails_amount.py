# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-15 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0017_auto_20180204_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]