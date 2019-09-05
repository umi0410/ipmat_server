from django.db import models
# from member.models import Member
from django.utils import timezone
from PIL import Image
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import StringIO, BytesIO
from django.core.files.base import ContentFile
import boto3
import io

IMAGE_PATH="imgs/"
def imgUpload(instance, _name):
    return IMAGE_PATH+_name
# Create your models here.

class FoodSubCategory(models.Model):
    categoryName=models.CharField(max_length=15, unique=True)
    def __str__(self):
        return "["+str(self.id)+"] "+self.categoryName
class Food(models.Model):
    food_name=models.CharField(max_length=15, unique=True)
    category=models.ManyToManyField(FoodSubCategory, default=1, blank=False)
    img=models.ImageField(upload_to=imgUpload, default="imgs/default_food.png")
    price=models.IntegerField(default=1)
    desc=models.TextField(blank=True, max_length=300)
    oneline_desc=models.CharField( max_length=30)
    creator=models.CharField(blank=True, max_length=30)
    # foodbook=models.ManyToManyField(Tag)
    # category=models.ManyToManyField(Category)

    def __str__(self):
        return "Food["+str(self.id)+"] "+self.food_name
    def save(self):
        super().save()
        s3 = boto3.resource('s3', region_name='us-east-2')
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        fileLocation=str(self.img)
        fileFullName=fileLocation.split("/")[-1]
        fileName, extension=fileFullName.split(".")

        object = bucket.Object(fileLocation)

        file = default_storage.open(fileLocation, "rb")
        img=Image.open(file)
        width, height = img.size
        print(width, height)
        if width>1200 or height>1000:
            img.thumbnail((600,500), Image.ANTIALIAS)
            if extension=="jpg" or extension=="JPG":
                extension="jpeg"
            # Byte Buffer에 이미지 데이터를 담아
            buff=BytesIO()
            img.save(buff, format=extension, quality=100)
            img_content = ContentFile(buff.getvalue())
            # Django의 ContentFile로 맵핑해
            resizeLocation=IMAGE_PATH+fileName+"_small."+extension
            # default_storage를 이용해서 location, content로 저장
            default_storage.save(resizeLocation,img_content)
            # s3 file을 닫고 저장
            file.close()
            self.img=IMAGE_PATH+fileName+"_small."+extension
            print("!", img.size)
            super().save()

    
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