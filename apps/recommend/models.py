# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Xsjz(models.Model):
    r = models.FloatField(primary_key=True)
    c = models.FloatField()
    v = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'XSJZ'
        unique_together = (('r', 'c'),)


class Recommend(models.Model):
    user_id = models.FloatField(primary_key=True)
    movie_id = models.FloatField()
    recommend_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RECOMMEND'
        unique_together = (('user_id', 'movie_id'),)
