# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-27 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0014_auto_20180321_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daily',
            name='units',
        ),
        migrations.RemoveField(
            model_name='eat',
            name='units',
        ),
        migrations.AlterField(
            model_name='daily',
            name='type',
            field=models.CharField(choices=[('screen_time', 'Minutes on phone'), ('steps', 'Steps walked')], db_index=True, help_text='The type of daily metric.', max_length=15),
        ),
    ]
