# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_auto_20180309_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choose',
            field=models.CharField(choices=[('\u6295\u7968', '\u6295\u7968'), ('\u95ee\u7b54', '\u95ee\u7b54'), ('\u516c\u544a', '\u516c\u544a')], default='\u6295\u7968', max_length=15, verbose_name='\u7c7b\u578b'),
        ),
    ]
