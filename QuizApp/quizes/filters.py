import django_filters
from .models import Quiz


class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = ['name']