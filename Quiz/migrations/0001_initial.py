# Generated by Django 4.2.2 on 2023-11-23 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('idCarrera', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cuestionarios',
            fields=[
                ('idCuestionario', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ElegirRespuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='¿Es esta la pregunta correcta?')),
                ('texto', models.TextField(verbose_name='Texto de la respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto de la pregunta')),
                ('dificultad', models.IntegerField(null=True, verbose_name='Dificultad pregunta')),
                ('max_puntaje', models.DecimalField(decimal_places=2, default=3, max_digits=6, verbose_name='Maximo Puntaje')),
                ('tipo', models.TextField(verbose_name='Tipo de pregunta')),
                ('unidad', models.IntegerField(verbose_name='Unidad a la que pertenece')),
                ('cuestionario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.cuestionarios', verbose_name='Cuestionario')),
            ],
        ),
        migrations.CreateModel(
            name='QuizUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.TextField(verbose_name='Ip usuario')),
                ('nombre', models.TextField(null=True, verbose_name='Nombre del usuario')),
                ('puntaje_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='Puntaje Total')),
                ('num_p', models.IntegerField(default=0, verbose_name='Numero de  preguntas respondidas')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntasRespondidas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dificultad', models.IntegerField(null=True, verbose_name='Dificultad de la pregunta')),
                ('uso_ayuda', models.BooleanField(default=False, verbose_name='¿Utilizo ayuda?')),
                ('tiempo_pregunta', models.IntegerField(null=True, verbose_name='Tiempo de la pregunta')),
                ('correcta', models.BooleanField(default=False, verbose_name='¿Es esta la respuesta correcta?')),
                ('puntaje_obtenido', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Puntaje Obtenido')),
                ('nombreUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intentos_username', to='Quiz.quizusuario')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='Quiz.pregunta')),
                ('quizUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos', to='Quiz.quizusuario')),
                ('respuesta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Quiz.elegirrespuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Materias',
            fields=[
                ('idMateria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('ciclo', models.IntegerField()),
                ('idCarrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.carrera')),
            ],
        ),
        migrations.AddField(
            model_name='elegirrespuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='Quiz.pregunta'),
        ),
        migrations.AddField(
            model_name='cuestionarios',
            name='idMateria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.materias'),
        ),
        migrations.CreateModel(
            name='ComentarioUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(verbose_name='Comentario')),
                ('nombreUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comentario_username', to='Quiz.quizusuario')),
                ('quizUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentario', to='Quiz.quizusuario')),
            ],
        ),
        migrations.CreateModel(
            name='QuizUsuario_Cuestionarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiempo', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=45)),
                ('quiz_cuestionarios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.cuestionarios')),
                ('quiz_quizusuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.quizusuario')),
            ],
            options={
                'unique_together': {('quiz_quizusuario', 'quiz_cuestionarios')},
            },
        ),
    ]
