# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-11 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0024_plotdrink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='value',
            field=models.FloatField(db_index=True, help_text='The recorded value for the type of metric', null=True),
        ),
    ]
