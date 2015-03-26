# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0009_championmatchup_last_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='championmatchup',
            old_name='champion',
            new_name='champion_name',
        ),
    ]
