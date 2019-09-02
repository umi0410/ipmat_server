from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
# Create your views here.
from .models import *
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
def create(request):
    return 1
def read(request, _id):
    return HttpResponse(Food.objects.filter(id=_id).values())

def readAll(request):
    foods=Food.objects.all()
    foods_json = serializers.serialize('json', foods)
    return HttpResponse(foods_json, content_type='application/json')

def readFromFoodBook(request, foodBookId):
    foods=FoodBook.objects.get(id=foodBookId).food.all().order_by("?")
    foods_json = serializers.serialize('json', foods)
    print(foods_json)
    return HttpResponse(foods_json, content_type='application/json')
    
def readTemp(request):
    foods=Food.objects.order_by("?")[:8]
    foods_json = serializers.serialize('json', foods)
    return HttpResponse(foods_json, content_type='application/json')
def readRandom(request):
#     food=Food.objects.order_by("?")[:1]
    food=Food.objects.filter(id=19)     # 초밥임
    food_json = serializers.serialize('json', food)
    return HttpResponse(food_json, content_type='application/json')

def update(request):
        return 1
def delete(request):
    return 1

def commentRead(request, food_id):
    return HttpResponse(FoodComment.objects.filter(food=food_id).values())
def commentDelete(request):
    return 1
def foodBookRead(request, id):
    foodbook=FoodBook.objects.filter(id =id)
    foodbook_json = serializers.serialize('json', foodbook)
    return HttpResponse(foodbook_json, content_type='application/json')

@csrf_exempt
def foodBookReadAll(request):
    foodbooks=FoodBook.objects.all()
    foodbooks_json = serializers.serialize('json', foodbooks)
    return HttpResponse(foodbooks_json, content_type='application/json')