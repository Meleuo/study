# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-11-24 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_auto_20201124_0901'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={},
        ),
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.ManyToManyField(to='app01.Author'),
        ),
    ]
