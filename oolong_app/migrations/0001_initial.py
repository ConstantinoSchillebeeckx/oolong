# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 22:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, default=None)),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='AvailableResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(help_text='Score for given response; e.g. 4.')),
                ('label', models.TextField(help_text="Text label for given response; e.g. 'Several days'.")),
            ],
            options={
                'db_table': 'available_response',
            },
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='When the metric event occurred or began.')),
                ('item', models.CharField(choices=[('water', 'Water'), ('tea', 'Tea'), ('coffee', 'Coffee'), ('alcohol', 'Alcohol'), ('soda', 'Soda')], default='water', help_text='The type of item drunk.', max_length=9)),
                ('value', models.FloatField(blank=True, help_text='The recorded volume for the metric event.', null=True)),
                ('units', models.CharField(blank=True, choices=[('fl oz', 'Fluid Ounce')], help_text='Units associated with the <code>Value</code> field.', max_length=9, null=True)),
                ('has_caffeine', models.BooleanField(default=True, help_text='Whether the metric event contained caffeine.')),
                ('alone', models.BooleanField(default=True, help_text='Whether metric event occurred while being alone.')),
                ('notes', models.TextField(blank=True, help_text='Any extra notes associated with metric event.', null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'metric_drink',
            },
        ),
        migrations.CreateModel(
            name='Eat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='When the metric event occurred or began.')),
                ('end', models.DateTimeField(blank=True, help_text='When provided, defines a duration of the metric event by subtracting the <code>Start</code> field.', null=True)),
                ('item', models.TextField(blank=True, help_text='Description of any item eaten.', null=True)),
                ('value', models.FloatField(blank=True, help_text='The recorded calories for the metric event.', null=True)),
                ('units', models.CharField(blank=True, choices=[('cal', 'Cal')], help_text='Units associated with the <code>Value</code> field.', max_length=3, null=True)),
                ('alone', models.BooleanField(default=True, help_text='Whether metric event occurred while being alone.')),
                ('notes', models.TextField(blank=True, help_text='Any extra notes associated with metric event.', null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'metric_eat',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(help_text='The text for the question.')),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, unique=True)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'questionnaire',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, help_text='Date on which question was answered.')),
                ('question', models.ForeignKey(help_text='Question being answered/scored.', on_delete=django.db.models.deletion.PROTECT, to='oolong_app.Question')),
                ('response', models.ForeignKey(help_text='Response to given question.', on_delete=django.db.models.deletion.PROTECT, to='oolong_app.AvailableResponse')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'response',
            },
        ),
        migrations.CreateModel(
            name='Sleep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='When the metric occurred or began.')),
                ('end', models.DateTimeField(help_text='When provided, defines a duration of the metric by subtracting the <code>start</code> field.')),
                ('alone', models.BooleanField(default=True, help_text='Whether metric event occurred while being alone.')),
                ('notes', models.TextField(blank=True, help_text='Any extra notes associated with metric event.', null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'metric_sleep',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(help_text='Which questionnaire the particular question is associated with.', on_delete=django.db.models.deletion.PROTECT, to='oolong_app.Questionnaire'),
        ),
        migrations.AddField(
            model_name='availableresponse',
            name='questionnaire',
            field=models.ForeignKey(help_text='Questionnaire for which response applies; e.g. GAD-7.', on_delete=django.db.models.deletion.PROTECT, to='oolong_app.Questionnaire'),
        ),
        migrations.AlterUniqueTogether(
            name='availableresponse',
            unique_together=set([('label', 'questionnaire'), ('score', 'questionnaire')]),
        ),
    ]
