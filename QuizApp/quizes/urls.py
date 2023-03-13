from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('all_category', views.allcategory, name='allcategory'),
    path('<int:pk>/', views.quizView, name='quiz'),
    path('category/<str:pk>/', views.categoryView, name='categories'),
    path('create_quiz/', views.createquizView, name='create_quiz'),
]
