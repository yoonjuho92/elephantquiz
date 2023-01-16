from django.db import models
from django.contrib.auth.models import User

class Text(models.Model):
    # 난이도 정의
    first_order = "1,2학년"
    second_order = "3,4학년"
    third_order = "5,6학년"
    difficulty_choices = (
        (first_order, "1,2학년"),
        (second_order, "3,4학년"),
        (third_order, "5,6학년")
    )
    # text에 들어가야하는 항목
    subject = models.CharField(max_length=200)
    content = models.TextField()
    difficulty = models.CharField(max_length=20,
                                  choices=difficulty_choices,
                                  default=None)
    def __str__(self):
        return self.subject

class Question(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    choice1 = models.CharField(max_length=100)
    choice2 = models.CharField(max_length=100)
    choice3 = models.CharField(max_length=100, blank=True)
    choice4 = models.CharField(max_length=100, blank=True)
    choice5 = models.CharField(max_length=100, blank=True)
    answer = models.IntegerField()
    def __str__(self):
        return str(self.text)

class UserChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField()
    choice = models.CharField(max_length=100)
    choiceDate = models.DateField(auto_now=True)

    def __str__(self):
        return (self.user.username + ' ' + self.question.question)

class UserProfile(models.Model):
    first_order = "1,2학년"
    second_order = "3,4학년"
    third_order = "5,6학년"
    difficulty_choices = (
        (first_order, "1,2학년"),
        (second_order, "3,4학년"),
        (third_order, "5,6학년")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=difficulty_choices, default=None)
    def __str__(self):
        return self.user.username