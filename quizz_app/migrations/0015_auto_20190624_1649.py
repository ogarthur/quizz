# Generated by Django 2.1.7 on 2019-06-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz_app', '0014_auto_20190624_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test_category',
            field=models.CharField(default='0', max_length=150),
        ),
    ]
