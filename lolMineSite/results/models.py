from django.db import models

# Create your models here.

class PlayerSearch(models.Model):
	username = models.CharField(max_length=50)
	main_role = models.CharField(max_length=15)
	secondary_role = models.CharField(max_length=15)
	aggOverFar = models.FloatField(null=True, blank=True)
	aggOverSur = models.FloatField(null=True, blank=True)
	aggOverVis = models.FloatField(null=True, blank=True)
	farOverSur = models.FloatField(null=True, blank=True)
	farOverVis = models.FloatField(null=True, blank=True)
	surOverVis = models.FloatField(null=True, blank=True)
