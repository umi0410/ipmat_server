from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns = [
    path('read/<int:_id>', views.read),
    path('readAll', views.readAll),
    path('read/from/<int:foodBookId>', views.readFromFoodBook),
    path('readTemp', views.readTemp),
    path('readRandom', views.readRandom),
    path('create', views.create),
    path('update/<str:id>', views.update),
    path('delete/<str:id>', views.delete),
    path("comment/read/<int:food_id>", views.commentRead),
    # path("reply/create/<int:food_id>", views.createCommet),
    # path("reply/read/<int:food_id>", views.updateComment),
    path("comment/delete/<int:comment_id>", views.commentDelete),
    path("foodBook/read/<int:id>", views.foodBookRead),
    path("foodBook/readAll", views.foodBookReadAll)
]