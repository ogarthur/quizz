#-*- coding: utf-8 -*-

from django.db import models

class Question(models.Model):
    class Meta:
        pass

    question_text = undefined()
    correct = undefined()

     = models.ForeignKey('Test', on_delete=models.PROTECT)

