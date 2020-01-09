from django.contrib import admin
from .model.answer import Answer
from .model.quiz import Quiz, QuizUser, CategoryQuiz
from .model.question import Question, QuestionUser
# Register your models here.

admin.site.register(Answer)
admin.site.register([Question, QuestionUser])
admin.site.register([Quiz, QuizUser, CategoryQuiz])
