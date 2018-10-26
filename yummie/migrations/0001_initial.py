# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-25 19:58
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawEvents',
            fields=[
                ('timestamp', models.DateTimeField()),
                ('name', models.CharField(max_length=200)),
                ('event_type', models.CharField(max_length=25)),
                ('event_id', models.BigIntegerField(null=True)),
                ('user_id', models.BigIntegerField()),
                ('user_created_at', models.DateTimeField(null=True)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('target_type', models.CharField(max_length=20, null=True)),
                ('target_id', models.BigIntegerField(null=True)),
                ('referal', models.CharField(default='Undefined', max_length=20)),
                ('os', models.CharField(default='Undefined', max_length=20)),
                ('device', models.CharField(default='Undefined', max_length=50)),
                ('identifier', models.CharField(max_length=100)),
                ('pk_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UsersEvents',
            fields=[
                ('timestamp', models.DateTimeField()),
                ('name', models.CharField(max_length=200)),
                ('event_type', models.CharField(max_length=25)),
                ('event_id', models.BigIntegerField(null=True)),
                ('user_id', models.BigIntegerField()),
                ('user_created_at', models.DateTimeField(null=True)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('target_type', models.CharField(max_length=20, null=True)),
                ('target_id', models.BigIntegerField(null=True)),
                ('referal', models.CharField(default='Undefined', max_length=20)),
                ('os', models.CharField(default='Undefined', max_length=20)),
                ('device', models.CharField(default='Undefined', max_length=50)),
                ('identifier', models.CharField(max_length=100)),
                ('pk_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='usersevents',
            index=models.Index(fields=['-timestamp', 'event_type'], name='yummie_user_timesta_8a50f5_idx'),
        ),
        migrations.AddIndex(
            model_name='usersevents',
            index=models.Index(fields=['event_type'], name='yummie_user_event_t_27fa94_idx'),
        ),
        migrations.AddIndex(
            model_name='rawevents',
            index=models.Index(fields=['-timestamp', 'event_type'], name='yummie_rawe_timesta_8a9562_idx'),
        ),
        migrations.AddIndex(
            model_name='rawevents',
            index=models.Index(fields=['event_type'], name='yummie_rawe_event_t_a824da_idx'),
        ),
    ]
