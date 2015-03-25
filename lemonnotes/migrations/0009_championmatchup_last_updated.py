# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0008_auto_20150319_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='championmatchup',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
    ]
