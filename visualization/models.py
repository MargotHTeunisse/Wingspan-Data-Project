# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bird(models.Model):
    scientific_name = models.CharField(primary_key=True, max_length=50)
    nl_name = models.CharField(unique=True, max_length=50, null=True)
    victory_points = models.PositiveSmallIntegerField(default=0)
    lives_in_forest = models.IntegerField(null=True)
    lives_in_grasslands = models.IntegerField(null=True)
    lives_in_wetlands = models.IntegerField(null=True)
    nest_type = models.CharField(max_length=4, null=True)
    nest_capacity = models.PositiveSmallIntegerField(default=0)
    wingspan = models.PositiveSmallIntegerField(default=0)
    expansion = models.CharField(max_length=2, null=True)
    power = models.ForeignKey('Power', models.SET_NULL, null=True)
    food_is_multiple_choice = models.IntegerField(default=False)
    worms = models.PositiveSmallIntegerField(default=0)
    grains = models.PositiveSmallIntegerField(default=0)
    berries = models.PositiveSmallIntegerField(default=0)
    fish = models.PositiveSmallIntegerField(default=0)
    rats = models.PositiveSmallIntegerField(default=0)
    wild = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'bird'

class Power(models.Model):
    power_id = models.SmallAutoField(primary_key=True)
    color = models.CharField(max_length=2, null=True)
    type = models.CharField(max_length=4, null=True)
    description = models.CharField(max_length=250, null=True)

    class Meta:
        db_table = 'power'
