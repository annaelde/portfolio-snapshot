# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('mediamanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=64)),
                ('subtitle', models.CharField(blank=True, default='', max_length=64)),
                ('date', models.DateField(blank=True, null=True)),
                ('published', models.BooleanField(choices=[(False, 'Save as Draft'), (True, 'Publish to Portfolio')], default=False)),
                ('slug', models.SlugField(blank=True, default='', max_length=64, unique=True)),
                ('external_url', models.URLField(blank=True, default='')),
                ('repository', models.URLField(blank=True, default='')),
                ('category', models.IntegerField(choices=[(1, 'Web Development'), (2, 'Programming'), (3, 'Game Development')], default=1)),
                ('snippet', models.CharField(blank=True, default='', max_length=1024)),
                ('description', models.CharField(blank=True, default='', max_length=160)),
                ('content', models.TextField(blank=True, default='')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='TaggedProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.Project')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_taggedproject_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='portfolio.TaggedProject', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='project',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mediamanager.Image'),
        ),
    ]
