# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-17 00:17
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datetimes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_processed_timestamp', models.DateTimeField(blank=True, null=True)),
                ('command', models.CharField(max_length=20, null=True)),
                ('associated_table', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventPaths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=2000)),
                ('registered', models.BooleanField()),
                ('request', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('response', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JsonEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('request_dict', django.contrib.postgres.fields.jsonb.JSONField()),
                ('response_dict', django.contrib.postgres.fields.jsonb.JSONField()),
                ('inserted_at', models.DateTimeField(auto_now_add=True)),
                ('identifier', models.CharField(max_length=100)),
            ],
        ),
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
            index=models.Index(fields=['-timestamp', 'event_type'], name='s3pooler_us_timesta_62d4b6_idx'),
        ),
        migrations.AddIndex(
            model_name='usersevents',
            index=models.Index(fields=['event_type'], name='s3pooler_us_event_t_a643d8_idx'),
        ),
        migrations.AddIndex(
            model_name='rawevents',
            index=models.Index(fields=['-timestamp', 'event_type'], name='s3pooler_ra_timesta_b8d3d4_idx'),
        ),
        migrations.AddIndex(
            model_name='rawevents',
            index=models.Index(fields=['event_type'], name='s3pooler_ra_event_t_bcfe0b_idx'),
        ),
        migrations.AddIndex(
            model_name='jsonevents',
            index=models.Index(fields=['timestamp'], name='s3pooler_js_timesta_fd28df_idx'),
        ),
    ]
