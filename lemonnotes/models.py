from django.db import models
from solo.models import SingletonModel
from jsonfield import JSONField
from datetime import datetime

# Create your models here.


# Not currently used. Will probably be used later.
class Summoner(models.Model):
    idNumber = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=8)


class Realms(SingletonModel):
    v = models.CharField(max_length=64, default='')
    dd = models.CharField(max_length=64, default='')
    cdn = models.CharField(max_length=255, default='')
    lg = models.CharField(max_length=64, default='')
    n = JSONField(default={})
    profile_icon_max = models.IntegerField(default=0)
    l = models.CharField(max_length=64, default='')
    css = models.CharField(max_length=64, default='')
    last_updated = models.DateTimeField(auto_now=True, default=datetime.now)

    def __unicode__(self):
        return "Realms"

    class Meta:
        verbose_name = "Realms"


class Champion(models.Model):
    idNumber = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    key = models.CharField(max_length=128, default='')

    class Meta:
            verbose_name_plural = "Champions"


class ChampionMatchup(models.Model):
    champion = models.CharField(max_length=128, default='')
    role = models.CharField(max_length=16, default='')
    champions_that_counter = JSONField(default=[])
    champions_that_this_counters = JSONField(default=[])
    support_adcs_that_counter = JSONField(default=[])
    support_adcs_that_synergize_poorly = JSONField(default=[])
    support_adcs_that_this_counters = JSONField(default=[])
    support_adcs_that_synergize_well = JSONField(default=[])
    adc_supports_that_counter = JSONField(default=[])
    adc_supports_that_synergize_poorly = JSONField(default=[])
    adc_supports_that_this_counters = JSONField(default=[])
    adc_supports_that_synergize_well = JSONField(default=[])
    last_updated = models.DateTimeField(auto_now=True, default=datetime.now)
