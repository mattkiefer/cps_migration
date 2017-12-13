# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class CommArea(models.Model):
    name = models.CharField(null=True,max_length=40)
    comm_area_no = models.IntegerField(null=True)
    side = models.CharField(null=True,max_length=50)
    
    # census stuff:
    total_pop = models.IntegerField(null=True)

    pct_black = models.FloatField(null=True)
    pct_white = models.FloatField(null=True)
    pct_latino = models.FloatField(null=True)

    pct_poor = models.FloatField(null=True)
    
    age_under_5 = models.IntegerField(null=True)
    age_5_to_9 = models.IntegerField(null=True)
    age_10_to_14 = models.IntegerField(null=True)
    age_15_to_17 = models.IntegerField(null=True)
    age_18_to_19 = models.IntegerField(null=True)

