# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0004_auto_20150306_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idNumber', models.IntegerField(default=0, unique=True)),
                ('title', models.CharField(default=b'', max_length=128)),
                ('name', models.CharField(default=b'', max_length=128)),
                ('key', models.CharField(default=b'', max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Champions',
            },
            bases=(models.Model,),
        ),
    ]
