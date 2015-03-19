# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0006_championmatchups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championmatchups',
            name='champion',
            field=models.CharField(default=b'', max_length=128),
            preserve_default=True,
        ),
    ]
