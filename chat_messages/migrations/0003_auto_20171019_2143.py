# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 21:43
from __future__ import unicode_literals

import chat_messages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_messages', '0002_auto_20171019_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=chat_messages.models.file_directory),
        ),
        migrations.AlterField(
            model_name='messageimage',
            name='image',
            field=models.ImageField(upload_to=chat_messages.models.image_directory),
        ),
    ]
