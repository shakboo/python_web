# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 14:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20180309_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choiceAnswar',
            new_name='choiceAnswer',
        ),
    ]
