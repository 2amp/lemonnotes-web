# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0007_auto_20150319_0049'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChampionMatchups',
            new_name='ChampionMatchup',
        ),
    ]
