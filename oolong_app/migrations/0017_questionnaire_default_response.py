# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0016_auto_20180328_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='default_response',
            field=models.IntegerField(db_index=True, help_text='Default response with which to prepopulate question; references the ID of `available_response`.', null=True),
        ),
    ]
