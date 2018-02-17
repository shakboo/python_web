# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-17 14:16
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(blank=True, max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.CharField(choices=[('\u7b2c\u4e00\u6b21\u56de\u5f52', '\u7b2c\u4e00\u6b21\u56de\u5f52'), ('\u7b2c\u4e8c\u6b21\u56de\u5f52', '\u7b2c\u4e8c\u6b21\u56de\u5f52')], default='\u7b2c\u4e00\u6b21\u56de\u5f52', max_length=10, verbose_name='\u7b2c\u51e0\u6b21\u56de\u5f52')),
                ('rangen', models.CharField(choices=[('\u7070\u5ea6', '\u7070\u5ea6'), ('\u975e\u7070\u5ea6', '\u975e\u7070\u5ea6'), ('\u5c0f\u7ec4', '\u5c0f\u7ec4')], default='\u7070\u5ea6', max_length=10, verbose_name='\u8303\u56f4')),
                ('title', models.TextField(max_length=200, verbose_name='\u5185\u5bb9')),
                ('detail', models.TextField(blank=True, max_length=200, verbose_name='\u8865\u5145\u8bf4\u660e')),
                ('status', models.BooleanField(default=False, verbose_name='\u72b6\u6001')),
                ('handler', models.CharField(default='', max_length=10, verbose_name='\u786e\u8ba4\u4eba')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.DateField(verbose_name='\u5468\u7248\u672c')),
                ('leader', models.CharField(default='', max_length=10, verbose_name='\u503c\u5468\u4eba')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.AddField(
            model_name='context',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regress.Version'),
        ),
    ]
