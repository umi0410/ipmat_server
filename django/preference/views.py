# 이 앱의 설정과 관련한 REST API를 담당.
# class based view 와 다양한 http method 를 이용해보겠음.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView
from django.conf import settings

class S3Storage(View):
    def get(self,request):
        # print(request.__dir__())
        print(request.GET)
        if request.GET["type"] == "s3Host":
            s3Host=settings.AWS_S3_CUSTOM_DOMAIN
            data={"s3Host":s3Host}
            return JsonResponse(data, json_dumps_params={'ensure_ascii': True})

    # def get_data(self):
    #     return{
    #         'message' : '안녕 파이썬 장고',
    #         'items' : ['파이썬', '장고', 'AWS', 'Azure'],
    #     }
