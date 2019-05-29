#-*- coding: utf-8 -*-

from django.db import models

from .question import Question


class Answer(models.Model):
    class Meta:
        pass

    answer_text = models.TextField()
    correct_answer = models.BooleanField(default=False)

    answer_question = models.ForeignKey(Question,
                                        on_delete=models.CASCADE,
                                        related_name='answer_question')
    def __str__(self):
        return "{}=> {}".format(self.answer_question.question_text, self.answer_text)
