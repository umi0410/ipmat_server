from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns = [
    path('read/<str:prID>', views.read),
    path('readAll', views.readAll),
    path('create', views.create),
    path('update/<str:id>', views.update),
    path('addFavorite', views.addFavorite),
    path('delete/<str:id>', views.delete),
    path('login', views.login)
]