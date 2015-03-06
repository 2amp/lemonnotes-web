# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0002_realms'),
    ]

    operations = [
        migrations.AddField(
            model_name='realms',
            name='cdn',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='css',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='dd',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='l',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='lg',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='n',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='profile_icon_max',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='realms',
            name='v',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='summoner',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
