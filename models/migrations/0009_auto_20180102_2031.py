# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_auto_20180102_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='unique',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
