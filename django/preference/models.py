from django.db import models

# Create your models here.
class VisitorCount(models.Model):
    date=models.CharField(max_length=10)
    count=models.IntegerField(default=0)