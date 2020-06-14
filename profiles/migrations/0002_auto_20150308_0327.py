# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_id',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='screen_name',
            field=models.CharField(max_length=45, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='status',
            name='status_id',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
