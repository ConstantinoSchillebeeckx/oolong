# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oolong_app', '0010_auto_20180309_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='mood_score',
            field=models.IntegerField(blank=True, choices=[(1, 'Very unhappy'), (2, 'Unhappy'), (3, 'Neutral'), (4, 'Happy'), (5, 'Very happy')], db_index=True, help_text='Generalized mood for this metric.', null=True),
        ),
    ]
