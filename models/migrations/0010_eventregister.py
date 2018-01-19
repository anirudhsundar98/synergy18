# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_auto_20180102_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegister',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.EventDetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.UserDetails')),
            ],
        ),
    ]
