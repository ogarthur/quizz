#-*- coding: utf-8 -*-

from django.db import models

from .quiz import Quiz
from django.contrib.auth.models import User


class Question(models.Model):
    class Meta:
        pass

    question_text = models.TextField()
    question_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question_quiz')

    def __str__(self):
        return str(self.id)+"-"+self.question_text


class QuestionUser(models.Model):
    question_fails = models.IntegerField(default=0)
    question_hits = models.IntegerField(default=0)

    question_user = models.ForeignKey(User, related_name="question_user", on_delete=models.CASCADE)
    question_question = models.ForeignKey(Question, related_name="question_question", on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format( self.question_question)

    def question_ratio(self):
        if self.question_fails + self.question_hits > 0:
            if self.question_hits > 0:
                ratio = (self.question_hits / (self.question_hits + self.question_fails)) * 100
            else:
                ratio = 0
        else:
            ratio = 100
        return ratio
