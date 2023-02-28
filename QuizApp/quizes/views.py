from django.shortcuts import render
from .models import Quiz, Question, Answer


def quizView(request, pk):
    if request.method == 'GET':
        quizz = Quiz.objects.get(id=pk)
        questionn = Question.objects.filter(quiz=quizz.id)
        answers = []
        for quest in questionn:
            answerr = quest.answer_set.all()
            answers.append(answerr)

        context = {"quiz": quizz, 'question': questionn, 'answers': answers}
        return render(request, 'quiztemplate.html', context)

