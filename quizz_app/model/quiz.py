#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class CategoryQuiz(models.Model):

    category_name = models.CharField(max_length=150)

    def __str__(self):
        return "{}".format(self.category_name)


class Quiz(models.Model):

    quiz_category = models.CharField(max_length=150, default="0")
    quiz_name = models.TextField()
    quiz_description = models.TextField(blank=True)
    quiz_randomizable = models.BooleanField(default=False)
    quiz_penalization = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}".format(self.quiz_category, self.quiz_name)


class QuizUser(models.Model):
    quiz_attempts = models.IntegerField(default=0)
    quiz_avg_result = models.IntegerField(default=0)

    quiz_quiz = models.ForeignKey(Quiz, related_name="quiz_quiz", on_delete=models.CASCADE)
    quiz_user = models.ForeignKey(User, related_name="quiz_user", on_delete=models.CASCADE)

    def __str__(self):
        return "{}_{}:{}".format(self.id, self.quiz_quiz_id, self.quiz_user_id)

    def update_result(self, newresult):
        self.quiz_avg_result = (self.quiz_avg_result + newresult)/2

        return True
