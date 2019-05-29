from django.contrib import admin
from .model.answer import Answer
from .model.test import Test,TestUser
from .model.question import Question,QuestionUser
# Register your models here.

admin.site.register(Answer)
admin.site.register([Question,QuestionUser])
admin.site.register([Test,TestUser])
