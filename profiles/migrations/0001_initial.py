# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('profile_id', models.BigIntegerField()),
                ('screen_name', models.CharField(max_length=45)),
                ('name', models.CharField(max_length=45)),
                ('location', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=200)),
                ('profile_image_url', models.URLField()),
                ('_user_json', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status_id', models.BigIntegerField()),
                ('_status_json', models.TextField(blank=True)),
                ('profile', models.ForeignKey(to='profiles.Profile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
