from django.db import models
from food.models import FoodBook
# Create your models here.
def imgUpload(instance, _name):
    return "imgs/"+_name

class Member(models.Model):
    _id=models.CharField(max_length=15, primary_key=True)
    pw=models.CharField(max_length=20)
    session_key=models.CharField(default="", max_length=50)
    birth_year=models.IntegerField()
    favorite_book=models.ManyToManyField(FoodBook, blank=True)

    birth_month=models.IntegerField(default=1)
    birth_day=models.IntegerField(default=1)
    imgs=models.ImageField(upload_to=imgUpload, default="imgs/default_profile.png")
    # favorite_tag=models.ManyToManyField(Tag)
    #own_tag=models.ManyToManyField(Tag)
