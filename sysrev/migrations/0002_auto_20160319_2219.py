# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysrev', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher',
            name='forename',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='surname',
        ),
        migrations.AlterField(
            model_name='researcher',
            name='lastViewed',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
