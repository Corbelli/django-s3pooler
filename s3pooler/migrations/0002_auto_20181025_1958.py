# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-25 19:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('s3pooler', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RawEvents',
        ),
        migrations.DeleteModel(
            name='UsersEvents',
        ),
    ]
