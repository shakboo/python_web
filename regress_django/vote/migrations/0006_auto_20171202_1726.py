# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-02 09:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_auto_20171202_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='answerer',
            new_name='who_votes',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='answer_text',
        ),
    ]
