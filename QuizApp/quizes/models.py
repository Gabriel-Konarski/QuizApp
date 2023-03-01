from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=True)
    email = models.EmailField()
    level = models.IntegerField()
    progress = models.IntegerField()
    quests = models.ManyToManyField('Quiz', blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.progress > 100:
            self.level += 1
            self.progress -= 100
        super(Profile, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    level = models.IntegerField()

    def __str__(self):
        return self.name


class Question(models.Model):
    content = models.CharField(max_length=128)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Answer(models.Model):
    name = models.CharField(max_length=32)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name