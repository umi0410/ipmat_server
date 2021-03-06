"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from preference import views as preference_views

def defaultIndex(request):
    return HttpResponse("<h1>Ipmat. 오늘의 입맛은?</h1><h2>docker swarm mode</h2>")
def getSetting(request):
    data={}
    data["MEDIA_URL"]=settings.MEDIA_URL
    data["BUCKET_URL"]=settings.AWS_S3_CUSTOM_DOMAIN
    
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('about/', include("about.urls")), 
    path('', defaultIndex), 
    path('food/', include("food.urls")), 
    path("foodTest/", include("food_test.urls")),
    # path('help/', include("help.urls")), 
    path('member/', include("member.urls")), 
    path('preference', preference_views.S3Storage.as_view()),
    # path('register/', include("register.urls")), 
    # path('tag', include("tag.urls"))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
