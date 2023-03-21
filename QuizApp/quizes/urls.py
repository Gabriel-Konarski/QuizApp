from django.urls import path, reverse_lazy
from django.views.generic import DeleteView

from . import views
from .models import Quiz

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('allquizes/', views.allquizes, name='allquizes'),
    path('<int:pk>/', views.quizView, name='quiz'),
    path('category/<str:pk>/', views.categoryView, name='categories'),
    path('allcategories/', views.allcategories, name='allcategories'),
    path('account/', views.acountDetails, name='account'),
    path('update_quiz/<str:pk>/', views.update_quiz, name='update_quiz'),
    path('createquiz/<str:pk>/', views.createquizView, name='create_quiz'),
    path('<int:pk>/delete/', DeleteView.as_view(
        model=Quiz,
        success_url=reverse_lazy('account'),
        template_name='quizes/generic_delete.html'
    ), name='quiz-delete'),
]

