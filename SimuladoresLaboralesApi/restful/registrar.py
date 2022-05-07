from ..models import *
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import hashlib
import re


def validacionCorreo(email):
    try:
        validate_email(email)
    except ValidationError:
        return False

    return True


def passwordEncriptacion(password):
    encoded = password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()


def verificacionPassword(password):
    passwd = password
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,50}$"
    # compiling regex
    pat = re.compile(reg)
    # searching regex                 
    mat = re.search(pat, passwd)
    # validating conditions
    if mat:
        return (True)
    else:
        return (False)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registrarParticipante(request):

    email = request.data.get('email')
    passwd = request.data.get('password')
    if validacionCorreo(email=email) != True:
        return Response({'correo': 'invalido'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    ''' 
    if verificacionPassword(password=passwd) != True:
        return Response({'password': 'incorrecta'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    try:
        responsableEvaluador = Evaluador.objects.get(email=responsable)  
    except Evaluador.DoesNotExist: 
        return Response({'responsable': 'noExist'}, status=status.HTTP_404_NOT_FOUND) 
    '''

    # Creacion de nuevo participante
    encryptPW = passwordEncriptacion(password=passwd)

    data = {
        'email': request.data.get('email'),
        'password': encryptPW,
        'nombre': request.data.get('nombre'),
        'apellido': request.data.get('apellido'),
        'fechaNacimiento': request.data.get('fechaNacimiento'),
        'genero': request.data.get('genero'),
    }

    if request.data.get('role') == 'user':
        seriealizer = RegistroParticipanteSerializerObjects(data=data)

    elif request.data.get('role') == 'expert':
        seriealizer = RegistroEvaluadorSerializerObjects(data=data)
    else:
        return Response({"status": "not_role", "message": "Rol no autorizado"}, status=status.HTTP_400_BAD_REQUEST)

    if seriealizer.is_valid():
        seriealizer.save()
        try:
            if request.data.get('role') == 'user':
                for discapacidad in request.data.get('discapacidades'):
                    data = {
                        'gradoDeDiscapacidad': discapacidad['grado'],
                        'participante': seriealizer.data['id'],
                        'discapacidad': discapacidad['code']
                    }
                    discapacidadSerializer = DiscapacidadParticipanteSerializerObjects(data=data)
                    if discapacidadSerializer.is_valid():
                        discapacidadSerializer.save()
        except:
            pass
        return Response({"status": "registrado"}, status=status.HTTP_201_CREATED)

    return Response(seriealizer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registrarExperienciaLaboral(request):
    correoParticpante = request.data.get('correo')
    participante = ''
    try:
        participante = Participante.objects.get(email=correoParticpante)
    except Evaluador.DoesNotExist:
        return Response({'Participante': 'noExist'}, status=status.HTTP_404_NOT_FOUND)

    experiencia = {
        "idExperienciaLaboral": 0,
        "areaLaboral": request.data.get('areaLaboral'),
        "aniosDeExperiencia": (int)(request.data.get('aniosDeExperiencia')),
        "sectorEconomico": request.data.get('sectorEconomico'),
        "participante": participante.id
    }

    experienciaLaboral_serializer = ExperienciaLaboralSerializerObjects(data=experiencia)
    if experienciaLaboral_serializer.is_valid():
        experienciaLaboral_serializer.save()
        return Response(experienciaLaboral_serializer.data, status=status.HTTP_201_CREATED)

    return Response(experienciaLaboral_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registrarEvaluador(request):
    email = request.data.get('email')
    passwd = request.data.get('password')

    if validacionCorreo(email=email) != True:
        return Response({'correo': 'invalido'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if verificacionPassword(password=passwd) != True:
        return Response({'password': 'incorrecta'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Creacion de nuevo experto
    encryptPW = passwordEncriptacion(password=passwd)
    evaluadorRegistrar = {
        'email': request.data.get('email'),
        'password': encryptPW,
        'nombre': request.data.get('nombre'),
        'apellido': request.data.get('apellido'),
        'telefono': request.data.get('telefono'),
        'pais': request.data.get('pais'),
        'ciudad': request.data.get('ciudad'),
        'direccion': request.data.get('direccion'),
        'nivelDeFormacion': request.data.get('nivelDeFormacion'),
    }

    evaluadorRegistrar_serializer = EvaluadorSerializerObjects(data=evaluadorRegistrar)
    if evaluadorRegistrar_serializer.is_valid():
        evaluadorRegistrar_serializer.save()
        return Response({"status": "registrado"}, status=status.HTTP_201_CREATED)

    return Response(evaluadorRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
