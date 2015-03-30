# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0010_auto_20150326_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='image',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=True,
        ),
    ]
