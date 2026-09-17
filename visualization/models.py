from django.db import models

# Create your models here.

class Bird(models.Model):
    scientific_name = models.TextField(default="")

    def __str__(self):
        return self.scientific_name