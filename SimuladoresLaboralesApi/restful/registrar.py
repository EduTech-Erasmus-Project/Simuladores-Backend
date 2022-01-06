from django.shortcuts import render

from SimuladoresLaboralesApi.views import ParticipanteViewSet
from ..models import * 
from ..serializers import * 
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import JSONParser 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import hashlib
import re
from django.http import JsonResponse

def validacionCorreo(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    else:
        return True

def passwordEncriptacion(password):
    encryptPW = hashlib.sha256(password)
    return encryptPW

def verificacionPassword(password):
    passwd = password
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    # compiling regex
    pat = re.compile(reg)
    # searching regex                 
    mat = re.search(pat, passwd)
    # validating conditions
    if mat:
        return(True)
    else:
        return(False)
    
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registrarParticipante(request): 
    email = request.data.get('Email')
    password = request.data.get('Password')
    responsable = request.data.get('Responsable')
    responsableEvaluador = ''
    if validacionCorreo(email=email) != True:
        return Response({'correo': 'invalido'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
    if verificacionPassword(password=password) != True:
        return Response({'password': 'incorrecta'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        responsableEvaluador = Evaluador.objects.get(id=responsable)  
    except Evaluador.DoesNotExist: 
        return Response({'responsable': 'noExist'}, status=status.HTTP_404_NOT_FOUND) 
    
    #Creacion de nuevo participante
    encryptPW = passwordEncriptacion(password=password)
    particpanteRegistrar = {
        'email' : request.data.get('Email'),
        'password' : encryptPW,
        'nombre' : request.data.get('Nombre'),
        'apellido' : request.data.get('Apellido'),
        'telefono' : request.data.get('Telefono'),
        'pais' : request.data.get('Pais'),
        'ciudad' : request.data.get('Ciudad'),
        'direccion' : request.data.get('Direccion'),
        'gradoDeDiscapacidad' : request.data.get('GradoDeDiscapacidad'),
        'fechaNacimiento' : request.data.get('FechaNacimiento'),
        'carreraUniversitaria' : request.data.get('CarreraUniversitaria'),
        'genero' : request.data.get('Genero'),
        'numeroDeHijos' : request.data.get('NumeroDeHijos'),
        'estadoCivil' : request.data.get('EstadoCivil'),
        'estudiosPrevios' : request.data.get('EstudiosPrevios'),
        'codigoEstudiante' : request.data.get('CodigoEstudiante'),
        'nivelDeFormacion' : request.data.get('NivelDeFormacion'),
        'responsable' : responsableEvaluador.id
    }
    
    particpanteRegistrar_serializer = ParticipanteSerializerObjects(data=particpanteRegistrar)
    if particpanteRegistrar_serializer.is_valid():
        particpanteRegistrar_serializer.save()
        return Response(particpanteRegistrar_serializer.data, status=status.HTTP_201_CREATED) 
    
    return Response(particpanteRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        "idExperienciaLaboral" :0,
        "areaLaboral": request.data.get('areaLaboral'),
        "aniosDeExperiencia": (int) (request.data.get('aniosDeExperiencia')),
        "sectorEconomico": request.data.get('sectorEconomico'),
        "participante":participante.id
    }
     
    experienciaLaboral_serializer = ExperienciaLaboralSerializerObjects(data=experiencia)
    if experienciaLaboral_serializer.is_valid():
        experienciaLaboral_serializer.save()
        return Response(experienciaLaboral_serializer.data, status=status.HTTP_201_CREATED) 
    
    return Response(experienciaLaboral_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
