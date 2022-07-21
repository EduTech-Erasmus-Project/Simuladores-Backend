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


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registroRubrica(request):
    print(request.data)

    calificacion = request.data.get('calificacion')
    indicador = request.data.get('indicador')
    ejercitarioid = request.data.get('ejercitario_id')

    rubrica = Rubrica()
    rubrica.calificacion = calificacion
    rubrica.indicador = indicador
    rubrica. ejercitario_id = ejercitarioid

    try:
        rubrica.save()
        return Response({'registropregunta': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'registropregunta': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def editarRubrica(request):
    if (request.method == 'PUT'):
        id = request.data.get('id')
        print(request.data)

    try:
        rubrica = Rubrica.objects.get(id=id)

    except:
        return Response({'edit': 'notPossible'}, status=status.HTTP_404_NOT_FOUND)

    rubrica.calificacion = request.data.get('calificacion')
    rubrica.indicador = request.data.get('indicador')
    rubrica.ejercitario_id = request.data.get('ejercitario_id')

    try:
        rubrica.save()
        return Response({'edit': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'edit': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def recuperarRubrica(request, pk=None):
    if request.method == 'GET':
        rubrica = Rubrica.objects.get(id=pk)
        rubrica_serializar = RubricaTotal(rubrica)
        return Response(rubrica_serializar.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listaRubrica(request, pk=None):
    if request.method == 'GET':
        rubrica = Rubrica.objects.filter(ejercitario_id=pk)
        rubrica_serializar = RubricaTotal(rubrica, many=True)
        return Response(rubrica_serializar.data)

@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
def eliminarRubrica(request, pk=None):
    if request.method == 'DELETE':
        print(f'-------->{pk}')
        rubrica = Rubrica.objects.filter(id=pk)
        print(rubrica)
        rubrica.delete()

        rubrica_serializar = RubricaTotal(rubrica)
        return Response(rubrica_serializar.data)
