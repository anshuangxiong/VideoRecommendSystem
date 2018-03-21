# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Movies(models.Model):
    movie_id = models.FloatField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=5, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    genres_en = models.CharField(max_length=255, blank=True, null=True)
    m_desc = models.TextField(blank=True, null=True)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    movie_80_id = models.FloatField(blank=True, null=True)
    isnew = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MOVIES'


class Links(models.Model):
    movie_id = models.FloatField(primary_key=True)
    imbd_id = models.FloatField(blank=True, null=True)
    tmdb_id = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LINKS'


class Ratings(models.Model):
    user_id = models.FloatField(primary_key=True)
    movie_id = models.FloatField()
    rating = models.FloatField(blank=True, null=True)
    timestamp = models.CharField(max_length=100, blank=True, null=True)
    isupdate = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RATINGS'
        unique_together = (('user_id', 'movie_id'),)


class Tags(models.Model):
    user_id = models.FloatField(blank=True, null=True)
    movie_id = models.FloatField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TAGS'


class Sysusers(models.Model):
    user_id = models.FloatField(primary_key=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    hobby = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SYSUSERS'
