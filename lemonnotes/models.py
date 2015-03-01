from django.db import models

# Create your models here.


# Not currently used. Will probably be used later.
class Summoner(models.Model):
    idNumber = models.IntegerField(default=0)
    name = models.CharField(max_length=256)
    region = models.CharField(max_length=8)
