from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Quiz(models.Model):
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