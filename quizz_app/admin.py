from django.contrib import admin
from .model.answer import Answer
from .model.test import Test
from .model.question import Question
# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Test)
