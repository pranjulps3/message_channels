# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_messages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='messageimage',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]