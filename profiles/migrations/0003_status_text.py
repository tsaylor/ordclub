# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models, migrations


def forwards_func(apps, schema_editor):
    Status = apps.get_model("profiles", "Status")
    db_alias = schema_editor.connection.alias
    qs = Status.objects.using(db_alias).all()
    for s in qs:
        j = json.loads(s._status_json)
        if 'retweeted_status' in j:
            s.content = j['retweeted_status']['text']
        else:
            s.content = j['text']
        s.save()

def backwards_func(apps, schema_editor):
    Status = apps.get_model("profiles", "Status")
    Status.objects.all().update(content='')

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150308_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='content',         # \/ This is supposedly extremely slow. make nullable
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.RunPython(  # separate this into 0004 migration
            forwards_func,
            backwards_func,
        ),
    ]
