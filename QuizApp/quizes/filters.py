import django_filters
from django import forms
from .models import Quiz
from django import forms

# class QuizFilter(django_filters.FilterSet):
#     class Meta:
#         model = Quiz
#         fields = ['name']


class QuizFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'class': 'form-control pe-2 bg-transparent', 'placeholder': 'Search...', 'aria-label': 'Search'})
    )

    class Meta:
        model = Quiz
        fields = ['name']