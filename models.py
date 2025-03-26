from django.db import models

# Create your models here.
class polls(models.Model):
    pr_id = models.PositiveIntegerField()
    name=models.CharField(max_length=50)
    cost=models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateTimeField()
    desc = models.TextField()


def __str__(self):
    return self.name