from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns = [
    path('member/read/<str:id>', views.read),
    path('member/create', views.create),
    path('member/update/<str:id>', views.update),
    path('member/delete/<str:id>', views.delete)
]