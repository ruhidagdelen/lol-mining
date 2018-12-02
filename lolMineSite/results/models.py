from django.db import models

# Create your models here.

class Player(models.Model):
	username = models.CharField(max_length=50)
	main_role = models.CharField(max_length=15)
	secondary_role = models.CharField(max_length=15)

	
	

