# Generated by Django 4.1.1 on 2022-10-22 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0019_pregunta_dificultad'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='tipo',
            field=models.TextField(null=True, verbose_name='Tipo de pregunta'),
        ),
        migrations.AddField(
            model_name='pregunta',
            name='unidad',
            field=models.IntegerField(null=True, verbose_name='Unidad a la que pertenece'),
        ),
    ]