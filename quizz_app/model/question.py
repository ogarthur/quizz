#-*- coding: utf-8 -*-

from django.db import models

from .test import Test
from django.contrib.auth.models import User


class Question(models.Model):
    class Meta:
        pass

    question_text = models.TextField()
    question_test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='question_test')

    def __str__(self):
        return self.question_text


class QuestionUser(models.Model):
    question_fails = models.IntegerField(default=0)
    question_ok = models.IntegerField(default=0)

    question_user = models.ForeignKey(User, related_name="question_user", on_delete=models.CASCADE)
    question_question = models.ForeignKey(Question, related_name="question_question", on_delete=models.CASCADE)

    def __str__(self):
        return "{}_{}:{}".format(self.id, self.question_question_id, self.question_user_id)

    def question_ratio(self):
        if self.question_tries > 0:
            if self.question_ok > 0:
                ratio = (self.question_ok / (self.question_ok + self.question_fails)) * 100
            else:
                ratio = 0
        else:
            ratio = 100
        return ratio