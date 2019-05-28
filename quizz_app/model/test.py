#-*- coding: utf-8 -*-

from django.db import models
CATEGORY_CHOICES = (
    ('BLOQUE1', '1'),
    ('BLOQUE2', '2'),
    ('BLOQUE3', '3'),
    ('BLOQUE4', '4'),
    ('BLOQUE5', '5'),
    ('EXAMEN', '6'),
)


class Test(models.Model):
    class Meta:
        pass

    test_category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    test_name = models.TextField()
    test_description = models.TextField(blank=True)
    test_tries = models.IntegerField(default=0)
    test_ok = models.IntegerField(default=0)

    def test_ratio(self):
        if self.test_tries > 0 and self.test_ok>0:

                ratio = (self.test_ok/self.test_tries)*100
        else:
            ratio = 0

        return ratio

    def __str__(self):
        return "{}: {}".format(self.test_category, self.test_name)

