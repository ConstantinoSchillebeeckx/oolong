# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 23:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oolong_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='availableresponse',
            name='label',
            field=models.TextField(db_index=True, help_text="Text label for given response; e.g. 'Several days'."),
        ),
        migrations.AlterField(
            model_name='availableresponse',
            name='score',
            field=models.IntegerField(db_index=True, help_text='Score for given response; e.g. 4.'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='alone',
            field=models.BooleanField(db_index=True, default=True, help_text='Whether metric event occurred while being alone.'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='has_caffeine',
            field=models.BooleanField(db_index=True, default=True, help_text='Whether the metric event contained caffeine.'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='item',
            field=models.CharField(choices=[('water', 'Water'), ('tea', 'Tea'), ('coffee', 'Coffee'), ('alcohol', 'Alcohol'), ('soda', 'Soda')], db_index=True, default='water', help_text='The type of item drunk.', max_length=9),
        ),
        migrations.AlterField(
            model_name='drink',
            name='start',
            field=models.DateTimeField(db_index=True, help_text='When the metric event occurred or began.'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='units',
            field=models.CharField(blank=True, choices=[('fl oz', 'Fluid Ounce')], db_index=True, help_text='Units associated with the <code>Value</code> field.', max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='drink',
            name='value',
            field=models.FloatField(blank=True, db_index=True, help_text='The recorded volume for the metric event.', null=True),
        ),
        migrations.AlterField(
            model_name='eat',
            name='alone',
            field=models.BooleanField(db_index=True, default=True, help_text='Whether metric event occurred while being alone.'),
        ),
        migrations.AlterField(
            model_name='eat',
            name='end',
            field=models.DateTimeField(blank=True, db_index=True, help_text='When provided, defines a duration of the metric event by subtracting the <code>Start</code> field.', null=True),
        ),
        migrations.AlterField(
            model_name='eat',
            name='item',
            field=models.TextField(blank=True, db_index=True, help_text='Description of any item eaten.', null=True),
        ),
        migrations.AlterField(
            model_name='eat',
            name='start',
            field=models.DateTimeField(db_index=True, help_text='When the metric event occurred or began.'),
        ),
        migrations.AlterField(
            model_name='eat',
            name='units',
            field=models.CharField(blank=True, choices=[('cal', 'Cal')], db_index=True, help_text='Units associated with the <code>Value</code> field.', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='eat',
            name='value',
            field=models.FloatField(blank=True, db_index=True, help_text='The recorded calories for the metric event.', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(db_index=True, help_text='The text for the question.'),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='description',
            field=models.TextField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='date',
            field=models.DateField(auto_now_add=True, db_index=True, help_text='Date on which question was answered.'),
        ),
        migrations.AlterField(
            model_name='sleep',
            name='alone',
            field=models.BooleanField(db_index=True, default=True, help_text='Whether metric event occurred while being alone.'),
        ),
        migrations.AlterField(
            model_name='sleep',
            name='end',
            field=models.DateTimeField(db_index=True, help_text='When provided, defines a duration of the metric by subtracting the <code>start</code> field.'),
        ),
        migrations.AlterField(
            model_name='sleep',
            name='start',
            field=models.DateTimeField(db_index=True, help_text='When the metric event occurred or began.'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('question', 'questionnaire')]),
        ),
        migrations.AlterUniqueTogether(
            name='response',
            unique_together=set([('user', 'date', 'question', 'response')]),
        ),
    ]
