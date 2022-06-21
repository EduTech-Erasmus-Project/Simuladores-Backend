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


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarPregunta(request):
    if (request.method == 'PUT'):
        id = request.data.get('id')
        print(request.data)

    try:
        pregunta = Pregunta.objects.get(id=id)

    except:
        return Response({'edit': 'notPossible'}, status=status.HTTP_404_NOT_FOUND)

    pregunta.contenido = request.data.get('contenido')
    pregunta.respuestaCorrecta = request.data.get('respuestaCorrecta')
    pregunta.numeroPregunta = request.data.get('numeroPregunta')
    pregunta.preguntaDelEjercitario_id = request.data.get('preguntaDelEjercitario')

    try:
        pregunta.save()
        return Response({'edit': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'edit': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listaPreguntaEjercitario(request, pk=None):
    if request.method == 'GET':
        pregunta = Pregunta.objects.filter(preguntaDelEjercitario_id=pk)
        pregunta_serializar = PreguntaTotal(pregunta, many=True)
        return Response(pregunta_serializar.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def recuperarPreguntaEjercitario(request, pk=None):
    if request.method == 'GET':
        pregunta = Pregunta.objects.get(id=pk)
        pregunta_serializar = PreguntaTotal(pregunta)
        return Response(pregunta_serializar.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registroPregunta(request):
    print(request.data)
    numeroPregunta = request.data.get('numeroPregunta')
    contenido = request.data.get('contenido')
    respuestaCorrecta = request.data.get('respuestaCorrecta')
    preguntaDelEjercitario = request.data.get('id')

    pregunta = Pregunta()
    pregunta.numeroPregunta = numeroPregunta
    pregunta.contenido = contenido
    pregunta.respuestaCorrecta = respuestaCorrecta
    pregunta. preguntaDelEjercitario_id = preguntaDelEjercitario

    try:
        pregunta.save()
        return Response({'registropregunta': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'registropregunta': 'error'}, status=status.HTTP_400_BAD_REQUEST)
