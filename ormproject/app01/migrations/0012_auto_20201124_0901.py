# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-11-24 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_auto_20201124_0900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='age',
        ),
        migrations.RemoveField(
            model_name='author',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='author',
            name='sex',
        ),
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.ManyToManyField(to='app01.Author'),
        ),
    ]
