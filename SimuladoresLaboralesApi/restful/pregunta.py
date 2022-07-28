from ..mixins import IsAdmin
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
@permission_classes((IsAdmin,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarPregunta(request):

    id = request.data.get('id')


    try:
        pregunta = Pregunta.objects.get(id=id)

        print(pregunta)

    except:
        return Response({'edit': 'notPossible'}, status=status.HTTP_404_NOT_FOUND)

    try:
        pregunta.contenido = request.data.get('contenido')
        pregunta.respuestaCorrecta = request.data.get('respuestaCorrecta')
        pregunta.numeroPregunta = request.data.get('numeroPregunta')
        pregunta.preguntaDelEjercitario_id = request.data.get('preguntaDelEjercitario')
        pregunta.save()
        return Response({'edit': 'ok'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'edit': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAdmin,))
def listaPreguntaEjercitario(request, pk=None):
    if request.method == 'GET':
        pregunta = Pregunta.objects.filter(preguntaDelEjercitario_id=pk).order_by('id')
        pregunta_serializar = PreguntaTotal(pregunta, many=True)
        return Response(pregunta_serializar.data)


@api_view(['GET'])
@permission_classes((IsAdmin,))
def recuperarPreguntaEjercitario(request, pk=None):
    if request.method == 'GET':
        pregunta = Pregunta.objects.get(id=pk)
        pregunta_serializar = PreguntaTotal(pregunta)
        return Response(pregunta_serializar.data)

@api_view(['DELETE'])
@permission_classes((IsAdmin,))
def eliminarPregunta(request, pk=None):
    try:
        #print(f'-------->{pk}')
        pregunta = Pregunta.objects.get(id=pk)
        ejercitario = pregunta.preguntaDelEjercitario_id
        pregunta.delete()
        # pregunta.save()

        preguntas = Pregunta.objects.filter(preguntaDelEjercitario_id=ejercitario).order_by('id')
        print("data 0", preguntas[0].id)

        num = 1
        for p in preguntas:
            print("prev numero", p.numeroPregunta)
            p.numeroPregunta = num
            num += 1
            p.save()
            print("current numero", p.numeroPregunta)


        pregunta_serializar = PreguntaTotal(preguntas, many=True)
        return Response(pregunta_serializar.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"status": "error", "message": e.__str__()}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAdmin,))
def registroPregunta(request):
    try:
        for pregunta in request.data.get("questions"):
            #print(pregunta)
            seriealizer = PreguntaSerializer(data=pregunta)
            if seriealizer.is_valid():
                seriealizer.save()
        return Response({'registropregunta': 'ok', "data": request.data.get("questions")}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'registropregunta': 'error', "message": e.__str__()}, status=status.HTTP_400_BAD_REQUEST)