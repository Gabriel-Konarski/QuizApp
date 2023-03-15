from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=True)
    level = models.IntegerField(default=1)
    progress = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    # Create profile when user is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, name=instance.username)


    # Save profile whenever user is saved
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # Check if levelup is available
    def save(self, *args, **kwargs):
        if self.progress >= 100:
            self.level += 1
            self.progress -= 100
        super(Profile, self).save(*args, **kwargs)


class DoneQuizes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    points = models.IntegerField()

    date_completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.quiz}'


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField()
    description = models.TextField()
    completed_num = models.IntegerField(null=True, default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey('Type', null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)

    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



class Question(models.Model):
    content = models.CharField(max_length=128)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Answer(models.Model):
    name = models.CharField(max_length=32)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content