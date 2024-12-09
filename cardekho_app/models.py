from django.db import models

# Create your models here.
class car_list(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)
    active = models.BooleanField(default=False)