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
import hashlib

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def verificarExistenciaCorreo(request): 
    correo = request.data.get('correo')
    tipoUserParticipante = ''
    tipoUserEvaluador = ''
    try: 
        tipoUserParticipante = Participante.objects.get(email=correo) 
    except Participante.DoesNotExist: 
        print("Error en busqueda de correo en participantes")
    try:
        tipoUserEvaluador = Evaluador.objects.get(email=correo)  
    except Evaluador.DoesNotExist: 
        print("Error en busqueda de correo en evaluadores")
    
    if(tipoUserParticipante != ''):
        return Response({'tipoUsuario': 'participante'}, status=status.HTTP_200_OK) 
    elif (tipoUserEvaluador != ''):
        return Response({'tipoUsuario': 'evaluador'}, status=status.HTTP_200_OK) 
    else:
        return Response({'tipoUsuario': 'notExist'}, status=status.HTTP_404_NOT_FOUND) 

def passwordEncriptacion(password):
    encoded=password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def loginAcceso(request): 
    correo = request.data.get('correo')
    password = request.data.get('password')
    tipoUser = request.data.get('tipoUsuario')
    passwd = passwordEncriptacion(password)
    if(tipoUser == 'participante'):
        try:
            participante = Participante.objects.get(email=correo, password = passwd) 
            return Response({'login': 'true', 'correo': participante.email}, status=status.HTTP_200_OK) 
        except Participante.DoesNotExist: 
            return Response({'login': 'false'}, status=status.HTTP_404_NOT_FOUND) 
        
    elif(tipoUser == 'evaluador'):
        try:
            acceso = Evaluador.objects.get(email=correo, password = password) 
            return Response({'login': 'true', 'correo': acceso.email}, status=status.HTTP_200_OK) 
        except Evaluador.DoesNotExist: 
            return Response({'login': 'false'}, status=status.HTTP_404_NOT_FOUND) 
