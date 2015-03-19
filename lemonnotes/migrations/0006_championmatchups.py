# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lemonnotes', '0005_champion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChampionMatchups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('champion', models.CharField(default=b'', unique=True, max_length=128)),
                ('role', models.CharField(default=b'', max_length=16)),
                ('champions_that_counter', jsonfield.fields.JSONField(default=[])),
                ('champions_that_this_counters', jsonfield.fields.JSONField(default=[])),
                ('support_adcs_that_counter', jsonfield.fields.JSONField(default=[])),
                ('support_adcs_that_synergize_poorly', jsonfield.fields.JSONField(default=[])),
                ('support_adcs_that_this_counters', jsonfield.fields.JSONField(default=[])),
                ('support_adcs_that_synergize_well', jsonfield.fields.JSONField(default=[])),
                ('adc_supports_that_counter', jsonfield.fields.JSONField(default=[])),
                ('adc_supports_that_synergize_poorly', jsonfield.fields.JSONField(default=[])),
                ('adc_supports_that_this_counters', jsonfield.fields.JSONField(default=[])),
                ('adc_supports_that_synergize_well', jsonfield.fields.JSONField(default=[])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
