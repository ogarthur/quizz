#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('ALL' , 0),
    ('BLOQUE1', 1),
    ('BLOQUE2', 2),
    ('BLOQUE3', 3),
    ('BLOQUE4', 4),
    ('BLOQUE5', 5),
    ('EXAMEN', 6),
)


class Test(models.Model):
    class Meta:
        pass

    test_category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    test_name = models.TextField()
    test_description = models.TextField(blank=True)



    def __str__(self):
        return "{}: {}".format(self.test_category, self.test_name)


class TestUser(models.Model):
    test_fails = models.IntegerField(default=0)
    test_ok = models.IntegerField(default=0)

    test_test = models.ForeignKey(Test, related_name="test_test", on_delete=models.CASCADE)
    test_user = models.ForeignKey(User, related_name="test_user", on_delete=models.CASCADE)

    def  __str__(self):
        return "{}_{}:{}".format(self.id,self.test_test_id,self.test_user_id)

    def test_ratio(self):
        if self.test_fails + self.test_ok > 0:

                ratio = (self.test_ok/(self.test_fails + self.test_ok))*100
        else:
            ratio = 0

        return ratio