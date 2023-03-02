from django.forms import ModelForm
from .models import Quiz, Question, Answer


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"