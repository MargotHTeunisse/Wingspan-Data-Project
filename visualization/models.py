from django.db import models

# Create your models here.

class Bird(models.Model):
    scientific_name = models.TextField(default="")