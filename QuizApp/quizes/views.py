from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from random import shuffle

from .models import Quiz, Question, Answer, Profile, Category, DoneQuizes, Type, Comment
from .filters import QuizFilter


def quizView(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    questions = list(Question.objects.filter(quiz=quiz))
    comments = Comment.objects.filter(quiz=quiz).order_by('-added')

    shuffle(questions)

    quizes = Quiz.objects.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs

    if request.method == 'GET':
        context = {'quizes': quizes, 'myFilter': myFilter, "quiz": quiz, "questions": questions, 'done': False, 'comments': comments}


        if quiz.type == Type.objects.get(name='Checkbox'):
            answers = [list(question.answer_set.all()) for question in questions]
            for answer in answers:
                shuffle(answer)
            context['answers'] = answers
            return render(request, 'quizes/quiztemplate.html', context)

        elif quiz.type == Type.objects.get(name='KeyValue'):
            return render(request, 'quizes/key_value_quiz.html', context)


    elif request.method == 'POST':
        pts = 0
        max_points = 0
        data = request.POST
        user = request.user
        profile = Profile.objects.get(user=user)
        levelup_flag = False

        try:
            best_score = DoneQuizes.objects.get(user=profile, quiz=quiz)
        except:
            best_score = None

        if data.get('comment'):
            Comment.objects.create(content=data.get('comment'),
                                   quiz=quiz,
                                   author=profile)
            return redirect('quiz', pk=quiz.id)

        if quiz.type == Type.objects.get(name='Checkbox'):
            template_name = 'quizes/quiztemplate.html'
            type = 'checkbox'
            for question in questions:
                max_points += 1
                answer = get_object_or_404(Answer, id=data.get(str(question.id)))
                if answer.correct:
                    pts += 1

        elif quiz.type == Type.objects.get(name='KeyValue'):
            template_name = 'quizes/key_value_quiz.html'
            type = 'keyvalue'
            for question in questions:
                max_points += 1
                answer = get_object_or_404(Answer, question=question)
                if data[str(question.id)] == answer.name:
                    pts += 1


        max_points *= quiz.level
        points = pts*quiz.level

        if user != 'AnonymousUser':
            profil = Profile.objects.get(user=user)

            try:
                check_done_quiz = DoneQuizes.objects.get(
                    user=profil,
                    quiz=quiz
                )

            except:
                check_done_quiz = False

            if not check_done_quiz:
                done_quiz = DoneQuizes.objects.create(
                    user=profil,
                    quiz=quiz,
                    points=points
                )

                if quiz.author != profil:
                    profil.progress += points
                    if profil.progress >= 100:
                        levelup_flag = True
                    profil.save()

                    quiz.completed_num += 1
                    quiz.save()

            else:
                if check_done_quiz.points < points:
                    if quiz.author != profil:
                        profil.progress += points - check_done_quiz.points
                        if profil.progress >= 100:
                            levelup_flag = True
                        profil.save()
                    check_done_quiz.points = points
                    check_done_quiz.save()

        answers = [question.answer_set.all() for question in questions]
        context = {'points': points, 'max_points': max_points, 'levelup_flag': levelup_flag, 'done': True,
                   "quiz": quiz, "questions": questions, 'answers': answers, 'comments': comments,
                   'best_score': best_score}

        return render(request, template_name, context)


def home(request):
    users = Profile.objects.all().order_by('-level', '-progress')[:3]
    quizes = Quiz.objects.all().order_by('-added')[:3]
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs

    context = {'users': users, 'quizes': quizes, 'myFilter': myFilter}
    return render(request, 'quizes/home.html', context)


def users(request):
    users = Profile.objects.all().order_by('-level', '-progress')
    context = {'users': users}
    return render(request, 'quizes/users.html', context)


def allcategory(request):
    category = Category.objects.all()
    quizes = Quiz.objects.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    if not myFilter.is_bound:
        myFilter.form = myFilter.form.__class__(request.GET)
    quizes = myFilter.qs
    p = Paginator(quizes, 1)
    page = request.GET.get('page')
    quizes_list = p.get_page(page)
    nums = " " * quizes_list.paginator.num_pages
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
        'querystring': querystring.urlencode(),
        'nums': nums
    }
    return render(request, 'quizes/all_category.html', context)


@login_required
def update_quiz(request, pk):
    quiz = Quiz.objects.get(id=pk)
    quizes = Quiz.objects.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile != quiz.author:
        return redirect('home')

    questions = Quiz.objects.get(id=pk).question_set.all()
    categories = Category.objects.all()
    levels = (1, 2, 3, 4, 5, 6)
    answers = [question.answer_set.all() for question in questions]

    if request.method == 'POST':
        quiz.name = request.POST.get('quiz_name')
        quiz.description = request.POST.get('quiz_description')
        quiz.category_id = request.POST.get('category')
        quiz.level = request.POST.get('level')
        quiz.save()
        for question in questions:
            question.content = request.POST.get(f'question_{question.id}')
            question.save()

            selected_answer_id = request.POST.get(f'question_{question.id}_answer')
            for answer in question.answer_set.all():
                answer_name = request.POST.get(f'answer_{answer.id}')
                answer_correct = answer.id == int(selected_answer_id)

                answer.name = answer_name
                answer.correct = answer_correct
                answer.save()

        return redirect('quiz', pk=quiz.id)

    context = {'quiz': quiz, 'questions': questions, 'answers': answers, 'categories': categories, 'levels': levels, 'quizes': quizes, 'myFilter': myFilter}
    return render(request, 'quizes/update_quiz.html', context)


def categoryView(request, pk):
    category = Category.objects.get(id=pk)
    quizes = category.quiz_set.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs
    context = {'category': category, 'quizes': quizes, 'myFilter': myFilter}
    return render(request, 'quizes/category.html', context)


@login_required
def createquizView(request, pk):
    categories = Category.objects.all()
    type = get_object_or_404(Type, id=pk)
    quizes = Quiz.objects.all()
    myFilter = QuizFilter(request.GET, queryset=quizes)
    quizes = myFilter.qs
    levels = (1, 2, 3, 4, 5, 6)
    user = request.user
    profil = Profile.objects.get(user=user)
    if profil.level < 5:
        return render(request, 'quizes/too_small_lvl.html', {})
    if request.method == "GET":
        context = {'quizes': quizes, 'myFilter': myFilter, 'categories': categories, 'levels': levels, 'done': False}
        if type.name == 'Checkbox':
            return render(request, 'quizes/create_quiz.html', context)
        else:
            return render(request, 'quizes/key_Value.html', context)
    if request.method == "POST":

        try:
            quizname = request.POST['quiz-name']
        except:
            quizname = None
        if quizname:
            category = Category.objects.get(name=request.POST['quiz-category'])
            quiz = Quiz.objects.create(author=profil, category=category,
                                    type=type,
                                    name=request.POST['quiz-name'],
                                    description=request.POST['quiz-description'],
                                    level=request.POST['quiz-level'])


        if type.name == 'KeyValue':

            for i in range(1, 6):
                question_content = request.POST.get(f"question{i}")
                answer_name = request.POST.get(f"answer{i}")

                question = Question.objects.create(quiz=quiz, content=question_content)
                answer = Answer.objects.create(question=question, name=answer_name, correct=True)
                return redirect('home')
        else:
            if quizname:
                question = Question.objects.create(quiz=quiz, content=request.POST['question'])
            else:
                quiz = Quiz.objects.filter(author=profil).order_by('-added')[:1]
                question = Question.objects.create(quiz=quiz[0], content=request.POST['question'])
            answer1 = Answer.objects.create(question=question, name=request.POST['answer1'], correct=request.POST.get('correct_answer') == '1')
            answer2 = Answer.objects.create(question=question, name=request.POST['answer2'], correct=request.POST.get('correct_answer') == '2')
            answer3 = Answer.objects.create(question=question, name=request.POST['answer3'], correct=request.POST.get('correct_answer') == '3')
            answer4 = Answer.objects.create(question=question, name=request.POST['answer4'], correct=request.POST.get('correct_answer') == '4')

            if len(Question.objects.filter(quiz=quiz)) == 5:
                return redirect('home')
            else:
                return render(request, 'quizes/create_quiz.html', {'done': True})


@login_required
def acountDetails(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    created_quizes = Quiz.objects.filter(author=profile)
    history_quizes = DoneQuizes.objects.filter(user=profile).order_by('date_completed')

    context = {'user': user, 'profile': profile, 'created_quizes': created_quizes, 'history_quizes': history_quizes}
    return render(request, 'quizes/account.html', context)

