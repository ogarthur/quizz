# Generated by Django 2.1.7 on 2019-05-30 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz_app', '0011_auto_20190531_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test_category',
            field=models.CharField(choices=[('ALL', 'ALL'), ('BLOQUE1', 'BLOQUE1'), ('BLOQUE2', 'BLOQUE2'), ('BLOQUE3', 'BLOQUE3'), ('BLOQUE4', 'BLOQUE4'), ('CONSTITUCION', 'CONSTITUCION'), ('EXAMEN', 'EXAMEN')], max_length=150),
        ),
    ]