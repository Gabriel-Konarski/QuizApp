from django.urls import path, reverse_lazy
from django.views.generic import DeleteView

from . import views
from .models import Quiz

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('all_category', views.allcategory, name='allcategory'),
    path('<int:pk>/', views.quizView, name='quiz'),
    path('category/<str:pk>/', views.categoryView, name='categories'),
    path('create_quiz/', views.createquizView, name='create_quiz'),
    path('add_question/<str:pk>/', views.add_question, name='add_question'),
    path('account/', views.acountDetails, name='account'),
    path('quiz/<int:pk>/delete/', DeleteView.as_view(
                                                    model=Quiz,
                                                    success_url=reverse_lazy('account'),
                                                    template_name='quizes/generic_delete.html'
                                                 ), name='quiz-delete'),
]
