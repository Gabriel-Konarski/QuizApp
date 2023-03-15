import django_filters
from .models import Quiz
from django import forms

# class QuizFilter(django_filters.FilterSet):
#     class Meta:
#         model = Quiz
#         fields = ['name']


class QuizFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        widget=forms.TextInput(
            attrs={'class': 'form-control pe-2 bg-transparent', 'placeholder': 'Search...', 'aria-label': 'Search'})
    )

    class Meta:
        model = Quiz
        fields = ['name']