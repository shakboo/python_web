# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-02 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0007_auto_20171202_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='who_votes',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='question',
            name='choose',
            field=models.CharField(choices=[('choose_vote', '\u6295\u7968'), ('choose_qa', '\u95ee\u7b54')], default='\u6295\u7968', max_length=15, verbose_name='\u7c7b\u578b'),
        ),
    ]
