#-*- coding: utf-8 -*-

from django.db import models

class Answer(models.Model):
    class Meta:
        pass

    answer_text = undefined()
    correct_answer = undefined()

     = models.ForeignKey('Question', on_delete=models.PROTECT)

