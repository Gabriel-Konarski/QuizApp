from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('<int:pk>/', views.quizView, name='quiz'),
    path('category/<str:pk>/', views.categoryView, name='categories'),
    path('create_quiz/', views.createquizView, name='create_quiz'),
    path('create_question/<str:pk>', views.createquestionView, name='create_question'),
    path('create_answer/<str:pk>', views.createanswerView, name='create_answer'),
]
