from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
# Create your views here.
from .models import *
from food.models import *
from preference.models import *
from django.db import IntegrityError
import json
from django.views.decorators.csrf import csrf_exempt
import time, hashlib
import datetime

def read(request, prID):
    return HttpResponse(Member.objects.filter(_id=prID).values())
def readAll(request):
    members=Member.objects.all()
    members_json = serializers.serialize('json', members)
    return HttpResponse(members_json, content_type='application/json')

@csrf_exempt
def create(request):
    if request.method=="POST":
        print(request.POST)
        _id, pw= request.POST["id"], request.POST["pw"]
        birth_year=int(request.POST["birthYear"])
        try:
            Member(_id=_id, pw=pw).save()
            return HttpResponse("creation successed")
        except IntegrityError:
            # 에러 메시지로 바꾸기
            print("Duplicated values in creating an user")
            return HttpResponseBadRequest("duplicated values!")
        except Exception:
            return HttpResponseBadRequest("Some errors!")

    else:
        return HttpResponse("please use GET method")
def update(request):
    return 1

@csrf_exempt
def addFavorite(request):
    if request.method=="POST":
        try:
            print(request.POST)
            memberId, foodBookId = request.POST["memberId"], request.POST["foodBookId"]
            member = Member.objects.get(_id = memberId)
            print(member)
            member.favorite_book.add(FoodBook.objects.get(id=int(foodBookId)))
            # print(member+"에게 favorite "+FoodBook.objects.get(foodBookId)+"추가 중")
            member.save()
            return HttpResponse("favorite added")
        except:
            return HttpResponseBadRequest("wrong.")
    else:
        return HttpResponseBadRequest("wrong.")

        


def delete(request):
    return 1

@csrf_exempt
def login(request):
    if request.method=="POST":
        print(request.POST)
        print("인자")
        _id=None
        pw=None
        session=None

        # visitor count
        # 존재하지 않으면
        if(len(VisitorCount.objects.filter(date=datetime.date.today().strftime("%Y%m%d")))==0):
            vc=VisitorCount(date=datetime.date.today().strftime("%Y%m%d")).save()
        else:
            vc=VisitorCount.objects.get(date=datetime.date.today().strftime("%Y%m%d"))
            vc.count+=1
            vc.save()

        try:
            if "id" in request.POST.keys() and "pw" in request.POST.keys():
                _id, pw= request.POST["id"], request.POST["pw"]
                member=Member.objects.filter(_id=_id, pw=pw)

            elif "session_key" in request.POST.keys():
                _session=request.POST["session_key"]
                member=Member.objects.filter(session_key=_session)
            else :
                print("in views.py of Member. Login wrong...")
                member=[]
            if len(member) == 1:
                session_key=generateSessionKey()
                print("얻은 member")
                print(member)
                print(1)
                member.update(session_key=session_key)
                print(2)
                # 왠진 몰라도 그냥 member는 serialize가 안대네 session으로 로그인 했을 때는..?
                member_json = serializers.serialize('json', Member.objects.filter(session_key=session_key))
                print(member_json)
                return HttpResponse(member_json, content_type='application/json')
            else:
                print(4)
                return HttpResponseBadRequest("a wrong login trial!")

            
        except Exception:
            print(Exception)
            return HttpResponseBadRequest("Some errors!")

def generateSessionKey():
    sha = hashlib.sha1()
    sha.update(str(time.time()).encode()) 
    sessionkey = sha.hexdigest()
    print(sessionkey)
    return sessionkey

