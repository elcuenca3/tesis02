import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from Quiz.sistemafuzzy import sistemaFuzzy
from .forms import RegistroFormulario, UsuarioLoginFormulario
from .models import Carrera, QuizUsuario, Pregunta, PreguntasRespondidas, ElegirRespuesta, Materias, Cuestionarios, QuizUsuario_Cuestionarios
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.serializers import serialize


array = []
sec = 1800
t_pregunta = 0
ultima = 0
pregunta = None
getP = True
bandera = False
nombre_usuario = ''
tiempo_actual = timezone.now()
estado = "completo"
cuestionario_id= 1


def inicio(request):
    return render(request, 'inicio.html')


def tablero(request):
    global nombre_usuario
    try:
        QuizUser = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
        n_preguntas = QuizUser.num_p
    except:
        n_preguntas = 0

    total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usaurios_quiz.count()

    context = {
        'user': nombre_usuario,
        'usuario_quiz': total_usaurios_quiz,
        'contar_user': contador
    }

    if n_preguntas >= 20:
        codigo = get_client_ip(request) + '.' + nombre_usuario
        context = {
            'user': nombre_usuario,
            'usuario_quiz': total_usaurios_quiz,
            'contar_user': contador,
            'codigo': 'Su código es: ' + codigo
        }

    return render(request, 'play/tablero.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def resultado(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida,


    }
    return render(request, 'play/resultado.html', context)
def resultado1(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida,


    }
    return render(request, 'play/resultado1.html', context)
def resultado2(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida,


    }
    return render(request, 'play/resultado2.html', context)


def sinTiempo(request):

    return render(request, 'play/sinTiempo.html')


def comentario(request):

    QuizUser = QuizUsuario.objects.get(
        usuario=get_client_ip(request), nombre=nombre_usuario)
    coment = request.POST.get('comentario')

    context = {
        'bandera': False
    }

    if request.method == 'POST':
        QuizUser.guardar_comentario(coment)
        context = {
            'bandera': True,
            'gracias': 'Gracias por tu comentario'
        }

    return render(request, 'comentario.html', context)


def materia(request):
    materias = Materias.objects.all()
    return render(request, 'materia.html', {'materias': materias})


def obtenerCorrecta(pregunta_id, respuesta):

    correcta = respuesta.objects.filter(
        pregunta=pregunta_id, correcta=True).get()

    return correcta

# pruebas


@login_required
def lista_carreras(request):
    carreras = Carrera.objects.all()
    return render(request, 'lista_carreras.html', {'carreras': carreras})


@login_required
def lista_materias(request, id_carrera):
    carrera = get_object_or_404(Carrera, pk=id_carrera)
    materias = Materias.objects.filter(idCarrera=carrera)
    return render(request, 'lista_materias.html', {'materias': materias})


@login_required
def lista_cuestionarios(request, id_materia):
    materia = get_object_or_404(Materias, pk=id_materia)
    cuestionarios = Cuestionarios.objects.filter(idMateria=materia)
    return render(request, 'lista_cuestionarios.html', {'cuestionarios': cuestionarios})


@login_required
def lista_preguntas(request, id_cuestionario):
    global cuestionario_id
    cuestionario = get_object_or_404(Cuestionarios, pk=id_cuestionario)
    cuestionario_id = cuestionario.idCuestionario
    preguntas = Pregunta.objects.filter(cuestionario_id=cuestionario)
    print(cuestionario_id)
    estado_incompleto = 'incompleto'
    global tiempo_actual
    if request.user.is_authenticated:
        usuario_actual = request.user  # Obtén el usuario actualmente autenticado
        quiz_usuario = QuizUsuario.objects.get_or_create(
            usuario=usuario_actual)[0]
        # Verifica si ya existe una entrada para evitar duplicados
        existe_entrada = QuizUsuario_Cuestionarios.objects.filter(
            quiz_quizusuario=quiz_usuario, quiz_cuestionarios=cuestionario).exists()
    # Lógica para crear una entrada en QuizUsuario_Cuestionarios
    quiz_usuario, created = QuizUsuario.objects.get_or_create(
        usuario=usuario_actual)
    if not QuizUsuario_Cuestionarios.objects.filter(quiz_quizusuario=quiz_usuario, quiz_cuestionarios=cuestionario).exists():
        nueva_entrada = QuizUsuario_Cuestionarios(
            quiz_quizusuario=quiz_usuario,
            quiz_cuestionarios=cuestionario,
            tiempo=tiempo_actual,  # Guardar la hora actual
            estado=estado_incompleto,
        )
        nueva_entrada.save()
    return render(request, 'lista_preguntas.html', {'cuestionarios': preguntas,'id_cuestionario': cuestionario_id})
    # return render(request, 'lista_preguntas.html', {'cuestionarios': preguntas})
    # return render(request, 'lista_preguntas.html', {'cuestionario': cuestionario})


# Importa los modelos y vistas necesarios al principio del archivo views.py

# ... (código existente)


def jugar(request, id_cuestionario):
    global array
    global sec
    global t_pregunta
    global ultima
    global getP
    global bandera
    global nombre_usuario
    global pregunta
    global cuestionario_id

    print("lo que llego")
    print(id_cuestionario)

    try:
        quiz_user = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
        print("existe")
    except QuizUsuario.DoesNotExist:
        print("no existe")
        quiz_user = QuizUsuario.objects.filter(
            usuario=get_client_ip(request)).last()
        nombre_usuario = quiz_user.nombre
    id_cues=id_cuestionario

    context = {
        'pregunta': pregunta,
        'n_pregunta': quiz_user.num_p + 1,
        'array': len(array),
        'id_cuestionario' : id_cues+1,
        'sec': sec,
    }
    if request.GET.get('bandera', False):
        bandera = True

    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        respuesta_pk = request.POST.get('respuesta_pk')

        if respuesta_pk is None:
            return render(request, 'play/jugar.html', context)

        ultima = t_pregunta
        quiz_user.crear_intentos(pregunta)
        pregunta_respondida = PreguntasRespondidas.objects.filter(
            quizUser=quiz_user, pregunta__pk=pregunta_pk).last()

        opcion_seleccionada = ElegirRespuesta.objects.get(pk=respuesta_pk)
        array.append(pregunta_respondida)

        dificultad = pregunta.dificultad

        calificacion = quiz_user.validar_intento(
            pregunta_respondida, opcion_seleccionada, dificultad, bandera, ultima)

        sistemaFuzzy(calificacion, ultima, bandera, dificultad)

        getP = True
        bandera = False
        if id_cues==2:
            return redirect('resultado1', pregunta_respondida.pk)
        if id_cues==3:
            return redirect('resultado2', pregunta_respondida.pk)
        else:
            return redirect('resultado', pregunta_respondida.pk)

    else:
        if len(array) <= 20 and getP:
            pregunta = quiz_user.obtener_nuevas_preguntas(id_cues+1)
            print("lo que llego 2")
            print(id_cues)
            if pregunta is None:
                return render(request, 'play/jugar.html', {'array': 20})
            getP = False
        else:
            # cuestionario = get_object_or_404(Cuestionarios, pk=id_cuestionario)
            # usuario_actual = request.user  # Obtén el usuario actualmente autenticado
            # quiz_usuario = QuizUsuario.objects.get_or_create(usuario=usuario_actual)[0]
            # existe_entrada = QuizUsuario_Cuestionarios.objects.filter(quiz_quizusuario=quiz_usuario, quiz_cuestionarios=cuestionario).exists()
            # if existe_entrada:
            #     nueva_entrada = QuizUsuario_Cuestionarios(
            #     tiempo=tiempo_actual,  # Guardar la hora actual
            #     estado=estado,
            # )
            #     nueva_entrada.save()
            context = {
                'n_pregunta': quiz_user.num_p + 1,
                'array': len(array),
                'sec': sec,
            }

    try:
        correcta = obtenerCorrecta(pregunta.id, ElegirRespuesta)
    except AttributeError:
        context = {
            'array': 20
        }
        return render(request, 'play/jugar.html', context)

    context = {
        'pregunta': pregunta,
        'n_pregunta': quiz_user.num_p + 1,
        'array': len(array),
        'sec': sec,
        'correcta': correcta,
    }

    sec = request.GET.get('sec', None)

    if sec is not None:
        t_pregunta = 1800 - int(sec) - ultima

    return render(request, 'play/jugar.html', context)

# login and register


def salir(request):
    logout(request)
    return redirect('inicio')


def register(request):

    data = {
        'form': RegistroFormulario()
    }

    if request.method == 'POST':
        user_creation_form = RegistroFormulario(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            try:
                QuizUsuario.objects.get_or_create(
                    usuario=get_client_ip(request), nombre=user_creation_form.cleaned_data['username'])
            except:
                context = {
                    'alerta': 'Ingrese otro nombre de usuario'
                }
                return render(request, 'registration/register.html', context)
            return redirect('inicio')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


def mostrar_preguntas(request, idrespueta):
    # Obtener la cadena JSON de preguntas filtradas almacenada en la sesión
    cuestionario = get_object_or_404(Cuestionarios, pk=idrespueta)
    preguntas = ElegirRespuesta.objects.filter(ElegirRespuesta_id=cuestionario)
    preguntas_json = request.session.get('preguntas_filtradas')

    # Convertir la cadena JSON a objetos Python (siempre y cuando sea válido)
    preguntas_filtradas = []
    if preguntas_json:
        preguntas_filtradas = json.loads(preguntas_json)

    # Pasar las preguntas filtradas a la plantilla HTML
    context = {
        'preguntas_filtradas': preguntas_filtradas
    }

    return render(request, 'prueba.html', context)


def mostrar(request, id_cuestionario):
    global array
    global sec
    global t_pregunta
    global ultima
    global getP
    global bandera
    global nombre_usuario
    global pregunta

    cuestionario = get_object_or_404(Cuestionarios, pk=id_cuestionario)
    preguntas = Pregunta.objects.filter(cuestionario_id=cuestionario)
    respuestas = ElegirRespuesta.objects.filter(
        pregunta__cuestionario_id=cuestionario)

    try:
        quiz_user = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
    except QuizUsuario.DoesNotExist:
        quiz_user = QuizUsuario.objects.filter(
            usuario=get_client_ip(request)).last()
        nombre_usuario = quiz_user.nombre
    context = {
        'preguntas': preguntas,
        'respuestas': respuestas,
        'indice_pregunta': 0  # Esto se utilizará para rastrear la pregunta actual
    }
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        respuesta_pk = request.POST.get('respuesta_pk')

        if respuesta_pk is None:
            return render(request, 'play/jugar.html', context)

        ultima = t_pregunta
        quiz_user.crear_intentos(pregunta)
        pregunta_respondida = PreguntasRespondidas.objects.filter(
            quizUser=quiz_user, pregunta__pk=pregunta_pk).last()

        opcion_seleccionada = ElegirRespuesta.objects.get(pk=respuesta_pk)
        array.append(pregunta_respondida)

        dificultad = pregunta.dificultad

        calificacion = quiz_user.validar_intento(
            pregunta_respondida, opcion_seleccionada, dificultad, bandera, ultima)

        sistemaFuzzy(calificacion, ultima, bandera, dificultad)

        getP = True
        bandera = False

        return redirect('resultado', pregunta_respondida.pk)

    else:
        if len(array) <= 20 and getP:
            pregunta = quiz_user.obtener_nuevas_preguntas()
            if pregunta is None:
                return render(request, 'play/jugar.html', {'array': 20})
            getP = False
        else:
            # cuestionario = get_object_or_404(Cuestionarios, pk=id_cuestionario)
            # usuario_actual = request.user  # Obtén el usuario actualmente autenticado
            # quiz_usuario = QuizUsuario.objects.get_or_create(usuario=usuario_actual)[0]
            # existe_entrada = QuizUsuario_Cuestionarios.objects.filter(quiz_quizusuario=quiz_usuario, quiz_cuestionarios=cuestionario).exists()
            # if existe_entrada:
            #     nueva_entrada = QuizUsuario_Cuestionarios(
            #     tiempo=tiempo_actual,  # Guardar la hora actual
            #     estado=estado,
            # )
            #     nueva_entrada.save()
            context = {
                'n_pregunta': quiz_user.num_p + 1,
                'array': len(array),
                'sec': sec,
            }

    return render(request, 'mostrar.html', context)
