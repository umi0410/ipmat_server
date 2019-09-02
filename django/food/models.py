from django.db import models
# from member.models import Member
from django.utils import timezone
def imgUpload(instance, _name):
    return "imgs/"+_name
# Create your models here.

class FoodSubCategory(models.Model):
    categoryName=models.CharField(max_length=15, unique=True)
class Food(models.Model):
    food_name=models.CharField(max_length=15, unique=True)
    category=models.ManyToManyField(FoodSubCategory, default=1, blank=False)
    img=models.ImageField(upload_to=imgUpload, default="imgs/default_food.png")
    price=models.IntegerField(default=1)
    desc=models.TextField(blank=True, max_length=300)
    oneline_desc=models.CharField(default="맛있는 음식", max_length=30)
    creator=models.CharField(blank=True, max_length=30)
    # foodbook=models.ManyToManyField(Tag)
    # category=models.ManyToManyField(Category)

    def __str__(self):
        return "Food["+str(self.id)+"] "+self.food_name

    
class FoodBook(models.Model):
    food_book_name=models.CharField(max_length=30, unique=True)
    image=models.ImageField(default="imgs/food_book_default.jpg",
        upload_to=imgUpload, max_length=40)
    food=models.ManyToManyField(Food)
    star=models.IntegerField(default=0);
    # foodbook=models.ManyToManyField(Tag)
    # tag=models.ManyToManyField(Tag)
    # category=models.ManyToManyField(Category)
    def __str__(self):
        return "Foodbook["+str(self.id)+"] "+self.food_book_name