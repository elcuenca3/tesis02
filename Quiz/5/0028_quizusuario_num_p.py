# Generated by Django 4.1.1 on 2022-11-21 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0027_preguntasrespondidas_tiempo_pregunta'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizusuario',
            name='num_p',
            field=models.IntegerField(default=0, verbose_name='Numero de  preguntas respondidas'),
        ),
    ]