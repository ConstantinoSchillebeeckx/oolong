# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-31 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0020_auto_20180331_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='response',
            field=models.IntegerField(help_text='Response to given question.', null=True),
        ),
    ]
