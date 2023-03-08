from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Answer, User, DoneQuizes, Profile


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
        pts = 0
        max_points = 0
        data = request.POST
        user = request.user
        levelup_flag = False
        for quest in questionn:
            max_points += 1
            answer = get_object_or_404(Answer, id=data.get(str(quest.id)))
            if answer.correct:
                pts += 1

        max_points *=quizz.level
        points = pts*quizz.level

        if user != 'AnonymousUser':
            profil = Profile.objects.get(user=user)

            try:
                check_done_quiz = DoneQuizes.objects.get(
                    user=profil,
                    quiz=quizz
                )

            except:
                check_done_quiz = False

            if not check_done_quiz:
                done_quiz = DoneQuizes.objects.create(
                    user=profil,
                    quiz=quizz,
                    points=points
                )

                if quizz.author != profil:
                    profil.progress += points
                    if profil.progress >= 100:
                        levelup_flag = True
                    profil.save()

                    quizz.completed_num += 1
                    quizz.save()

            else:
                if check_done_quiz.points < points:
                    if quizz.author != profil:
                        profil.progress += points - check_done_quiz.points
                        if profil.progress >= 100:
                            levelup_flag = True
                        profil.save()
                    check_done_quiz.points = points
                    check_done_quiz.save()



        context = {'points': points, 'max_points': max_points, 'levelup_flag': levelup_flag}
        return render(request, 'quizes/points.html', context)


def home(request):
    users = User.objects.all().order_by('username').values()[:3]
    context = {'users': users}
    return render(request, 'quizes/home.html', context)


def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'quizes/users.html', context)
