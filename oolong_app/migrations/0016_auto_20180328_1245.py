# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0015_auto_20180327_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drink',
            old_name='value',
            new_name='volume',
        ),
        migrations.RenameField(
            model_name='eat',
            old_name='value',
            new_name='calories',
        ),
    ]