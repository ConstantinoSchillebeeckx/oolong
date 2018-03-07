# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0004_auto_20180306_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='type',
            field=models.CharField(choices=[('screen_time', 'Screen time'), ('steps', 'Steps')], db_index=True, help_text='The type of daily metric.', max_length=15),
        ),
    ]
