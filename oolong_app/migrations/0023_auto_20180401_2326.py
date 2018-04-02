# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-01 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0022_remove_response_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='mood',
            field=models.CharField(choices=[('happy', 'Happy'), ('anxious', 'Anxious'), ('depressed', 'Depressed'), ('sad', 'Sad'), ('lonely', 'Lonely'), ('generic', 'Generic')], db_index=True, help_text='General mood of this note.', max_length=10, null=True),
        ),
    ]