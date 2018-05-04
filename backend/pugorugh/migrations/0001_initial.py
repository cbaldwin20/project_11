# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-05-04 09:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image_filename', models.CharField(max_length=255)),
                ('breed', models.CharField(max_length=255)),
                ('age', models.IntegerField(help_text='integer for months')),
                ('age_category', models.CharField(max_length=255)),
                ('gender', models.CharField(help_text='“m” for male, “f” for female, “u” for unknown"', max_length=255)),
                ('size', models.CharField(help_text='"s" for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(help_text='“l” for liked, “d” for disliked', max_length=255)),
                ('amount_changed', models.IntegerField(default=0)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dog', to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(help_text='“b” for baby, “y” for young, “a” for adult, “s” for senior', max_length=255)),
                ('gender', models.CharField(help_text='“m” for male, “f” for female', max_length=255)),
                ('size', models.CharField(help_text='“s” for small, “m” for medium, “l” for large, “xl” for extra large', max_length=255)),
                ('amount_changed', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
