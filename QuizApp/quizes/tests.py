from django.test import Client
import pytest

""" URLS """
@pytest.mark.django_db
def test_homepage():

    client = Client()

    response = client.get('/quiz/', follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_users():

    client = Client()

    response = client.get('/quiz/users/', follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_all_category():
    client = Client()

    response = client.get('/quiz/all_category/', follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_createquiz():
    username = "test"
    password = "testpassword"
    user = User.objects.create_user(username=username, password=password)

    client = Client()
    client.login(username=username, password=password)
    profil = Profile.objects.get(user=user)
    profil.level = 5
    profil.save()

    response = client.get('/quiz/create_quiz/', follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_account():
    username = "test"
    password = "testpassword"
    user = User.objects.create_user(username=username, password=password)

    client = Client()
    client.login(username=username, password=password)

    response = client.get('/quiz/account/', follow=True)

    assert response.status_code == 200

"""DYNAMIC URLS"""
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Quiz, Category, Type, Profile

@pytest.mark.django_db
def test_quiz():
    client = Client()
    user = User.objects.create_user('pytest', 'pytest@gmail.com', 'pytestpassword')
    profile = Profile.objects.get(user=user)
    category = Category.objects.create(name='pytest')
    typ = Type.objects.create(name='Checkbox')
    quiz = Quiz.objects.create(name='pytest',
                               level=1,
                               description='test with pytest',
                               category=category,
                               type=typ,
                               author=profile)

    url = reverse('quiz', args=[quiz.id])
    response = client.get(url, follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_category():
    client = Client()
    category = Category.objects.create(name='pytest')

    url = reverse('categories', args=[category.id])
    response = client.get(url, follow=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_addquestion():
    username = "test"
    password = "testpassword"
    user = User.objects.create_user(username=username, password=password)

    client = Client()
    client.login(username=username, password=password)

    profile = Profile.objects.get(user=user)
    category = Category.objects.create(name='pytest')
    typ = Type.objects.create(name='Checkbox')
    quiz = Quiz.objects.create(name='pytest',
                               level=1,
                               description='test with pytest',
                               category=category,
                               type=typ,
                               author=profile)

    url = reverse('add_question', args=[quiz.id])
    response = client.get(url, follow=True)

    assert response.status_code == 200




""" MODELS """

@pytest.mark.django_db
def test_profileCreate():
    user = User.objects.create_user('pytest', 'pytest@gmail.com', 'haslomaslo')
    profile = Profile.objects.get(user=user)

    assert profile.name == 'pytest'


@pytest.mark.django_db
def test_profileLevelUp():
    user = User.objects.create_user('pytest', 'pytest@gmail.com', 'haslomaslo')
    profile = Profile.objects.get(user=user)
    profile.progress = 101
    profile.save()

    assert profile.level == 2
    assert profile.progress == 1



"""VIEWS"""
@pytest.mark.django_db
def test_homePageBestUsers():
    """
    This test assert that best users are in correct order and there are only 3 users
    :return:
    """
    user1 = User.objects.create_user('pytest1', 'pytest1@gmail.com', 'haslomaslo')
    user2 = User.objects.create_user('pytest2', 'pytest2@gmail.com', 'haslomaslo')
    user3 = User.objects.create_user('pytest3', 'pytest3@gmail.com', 'haslomaslo')
    user4 = User.objects.create_user('pytest4', 'pytest4@gmail.com', 'haslomaslo')

    users = [user1, user2, user3, user4]

    for idx, user in enumerate(users):
        profile = Profile.objects.get(user=user)
        profile.level = idx * 2
        profile.progress = idx * 12
        profile.save()

    client = Client()
    response = client.get('/quiz/')

    assert b'user1' not in response.content

    for user in users[1:]:
        assert b'user' in response.content
