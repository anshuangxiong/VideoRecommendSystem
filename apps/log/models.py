# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Movie80(models.Model):
    mid = models.CharField(primary_key=True, max_length=255)
    mname = models.CharField(max_length=255, blank=True, null=True)
    mname2 = models.CharField(max_length=255, blank=True, null=True)
    mactor = models.CharField(max_length=500, blank=True, null=True)
    mtype = models.CharField(max_length=255, blank=True, null=True)
    marea = models.CharField(max_length=255, blank=True, null=True)
    mlanguage = models.CharField(max_length=255, blank=True, null=True)
    mdirector = models.CharField(max_length=255, blank=True, null=True)
    mstartdate = models.CharField(max_length=255, blank=True, null=True)
    mlength = models.CharField(max_length=255, blank=True, null=True)
    mupdatedate = models.CharField(max_length=255, blank=True, null=True)
    mscore = models.CharField(max_length=255, blank=True, null=True)
    mintroduce = models.TextField(blank=True, null=True)
    mlink = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_80'
