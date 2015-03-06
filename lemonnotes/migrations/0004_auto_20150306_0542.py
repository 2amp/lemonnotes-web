# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0003_auto_20150306_0534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='realms',
            options={'verbose_name': 'Realms'},
        ),
        migrations.AddField(
            model_name='realms',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
    ]
