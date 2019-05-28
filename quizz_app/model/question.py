#-*- coding: utf-8 -*-

from django.db import models

from .test import Test


class Question(models.Model):
    class Meta:
        pass

    question_text = models.TextField()
    question_tries = models.IntegerField(default=0)
    question_ok = models.IntegerField(default=0)

    question_test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='question_test')

    def question_ratio(self):
        if self.question_tries > 0:
            if self.question_ok > 0:
                ratio = (self.question_ok / self.question_tries) * 100
            else:
                ratio = 0
        else:
            ratio = 100
        return ratio



    def __str__(self):
        return self.question_text