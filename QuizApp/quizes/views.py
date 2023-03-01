from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Answer


def quizView(request, pk):
    quizz = get_object_or_404(Quiz, id=pk)
    questionn = Question.objects.filter(quiz=quizz.id)

    if request.method == 'GET':
        answers = []
        for quest in questionn:
            answerr = quest.answer_set.all()
            answers.append(answerr)

        context = {"quiz": quizz, 'question': questionn, 'answers': answers}
        return render(request, 'quizes/quiztemplate.html', context)

    elif request.method == 'POST':
        points = 0
        max_points = 0
        data = request.POST
        for quest in questionn:
            max_points += 1
            print(quest.id)
            answer = get_object_or_404(Answer, id=data.get(str(quest.id)))
            if answer.correct:
                points += 1

        return render(request, 'quizes/points.html', {'points': points, 'max_points': max_points})