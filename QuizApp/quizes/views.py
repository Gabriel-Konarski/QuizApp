from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Answer, Profile, User, Category
from django.http import HttpResponse
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory

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

def home(request):
    category = Category.objects.all()
    users = Profile.objects.all().order_by('name').values()[:3]
    quizes = Quiz.objects.all().order_by('-added').values()[:5]
    context = {'users': users, 'quizes': quizes, 'category': category}
    return render(request, 'quizes/home.html', context)

def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'quizes/users.html', context)

def categoryView(request, pk):
    category = Category.objects.get(id=pk)
    quizes = category.quiz_set.all()
    context = {'category': category, 'quizes': quizes}
    return render(request, 'quizes/category.html', context)

def createquizView(request):
    form = QuizForm()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'quizes/create_quiz.html', context)

def createquestionView(request, pk):
    QuestionFormSet = inlineformset_factory(Quiz, Question, fields=('content', 'quiz'), extra=4)
    quiz = Quiz.objects.get(id=pk)
    formset = QuestionFormSet(queryset=Question.objects.none(), instance=quiz)
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, instance=quiz)
        if formset.is_valid():
            formset.save()
    context = {'formset': formset}
    return render(request, 'quizes/create_question.html', context)

def createanswerView(request,pk):
    AnswerFormSet = inlineformset_factory(Question, Answer, fields=('name', 'question', 'correct'), extra=2)
    question = Question.objects.get(id=pk)
    formset = AnswerFormSet(instance=question)
    if request.method == 'POST':
        formset = AnswerFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
    context = {'formset': formset}
    return render(request, 'quizes/create_answer.html', context)