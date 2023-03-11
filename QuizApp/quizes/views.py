from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, Profile, User, Category, DoneQuizes
from .filters import QuizFilter
from django.core.paginator import Paginator



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
    category = Category.objects.all()
    users = Profile.objects.all().order_by('name').values()[:3]
    quizes = Quiz.objects.all().order_by('-added').values()[:3]
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs
    context = {'users': users, 'quizes': quizes, 'category': category, 'myFilter': myFilter}
    return render(request, 'quizes/home.html', context)

def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'quizes/users.html', context)


def allcategory(request):
    category = Category.objects.all()
    quizes = Quiz.objects.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    if not myFilter.is_bound:
        myFilter.form = myFilter.form.__class__(request.GET)
    quizes = myFilter.qs
    p = Paginator(quizes, 2)
    page = request.GET.get('page')
    quizes_list = p.get_page(page)
    name = request.GET.get('name', '')
    querystring = request.GET.copy()
    if 'page' in querystring:
        del querystring['page']
    if name:
        querystring['name'] = name

    context = {
        'quizes_list': quizes_list,
        'myFilter': myFilter,
        'quizes': quizes,
        'category': category,
        'name': name,
        'querystring': querystring.urlencode()
    }
    return render(request, 'quizes/all_category.html', context)



def categoryView(request, pk):
    category = Category.objects.get(id=pk)
    quizes = category.quiz_set.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs
    context = {'category': category, 'quizes': quizes, 'myFilter': myFilter}
    return render(request, 'quizes/category.html', context)


def createquizView(request):
    if request.method == "GET":
        categories = Category.objects.all()
        levels =(1, 2, 3, 4, 5, 6)
        return render(request, 'quizes/create_quiz.html', {'categories': categories, 'levels': levels})

    if request.method == "POST":
        user = request.user
        category = Category.objects.get(name=request.POST['quiz-category'])
        profil = Profile.objects.get(user=user)
        quiz = Quiz.objects.create(author=profil, category=category,
                                   name=request.POST['quiz-name'],
                                   description=request.POST['quiz-description'],
                                   level=request.POST['quiz-level'])
        question = Question.objects.create(quiz=quiz, content=request.POST['question'])
        answer1 = Answer.objects.create(question=question, name=request.POST['answer1'], correct=request.POST.get('correct_answer') == '1')
        answer2 = Answer.objects.create(question=question, name=request.POST['answer2'], correct=request.POST.get('correct_answer') == '2')
        answer3 = Answer.objects.create(question=question, name=request.POST['answer3'], correct=request.POST.get('correct_answer') == '3')
        answer4 = Answer.objects.create(question=question, name=request.POST['answer4'], correct=request.POST.get('correct_answer') == '4')

        return redirect('add_question', pk=quiz.id)


def add_question(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.method == "GET":
        context = {'quiz': quiz}
        return render(request, 'quizes/add_question.html', context)

    if request.method == "POST":
        question = Question.objects.create(quiz=quiz, content=request.POST['question'])
        answer1 = Answer.objects.create(question=question, name=request.POST['answer1'], correct=request.POST.get('correct_answer') == '1')
        answer2 = Answer.objects.create(question=question, name=request.POST['answer2'], correct=request.POST.get('correct_answer') == '2')
        answer3 = Answer.objects.create(question=question, name=request.POST['answer3'], correct=request.POST.get('correct_answer') == '3')
        answer4 = Answer.objects.create(question=question, name=request.POST['answer4'], correct=request.POST.get('correct_answer') == '4')

        return redirect('add_question', pk=quiz.id)



