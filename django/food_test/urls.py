from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns = [
    path('read/<int:id>', views.read),
    path('readMyTest', views.readMyExamList),
    path('read/detail', views.readExamDetail),
    path('create/answer', views.createAnswer),
    path('question/read', views.readQuestion),
    path('result/read', views.readResult),
    path('result/score/read/<int:examId>', views.readScoreOfParticiapnts),
    path('participant/read', views.readParticipants),
    path('participant/delete', views.deleteParticipant),
    path('create', views.create),
    path('test/isExistFromHashId', views.isExistFromHashId),

    path('delete', views.deleteExam)

]