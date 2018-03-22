# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-21 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0013_auto_20180321_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='type',
            field=models.CharField(choices=[('screen_time', 'Time on phone'), ('steps', 'Distance walked')], db_index=True, help_text='The type of daily metric.', max_length=15),
        ),
    ]