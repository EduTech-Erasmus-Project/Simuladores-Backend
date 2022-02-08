from ast import Try
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
   
    if(tipoUserParticipante != '' and (tipoUserParticipante.estado=="activo") and (tipoUserParticipante.aceptacionPendianteResponsable=="aceptado")):
        return Response({'tipoUsuario': 'participante'}, status=status.HTTP_200_OK) 
    
    try: 
        tipoUserEvaluador = Evaluador.objects.get(email=correo) 
    except Evaluador.DoesNotExist: 
        print("Error en busqueda de correo en evaluador")
        
    if (tipoUserEvaluador != '' and (tipoUserEvaluador.estado=="activo")):
        return Response({'tipoUsuario': 'evaluador'}, status=status.HTTP_200_OK) 
    
    return Response({'tipoUsuario': 'notExist'}, status=status.HTTP_200_OK) 

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
        
    if(tipoUser == 'evaluador'):
        try:
            acceso = Evaluador.objects.get(email=correo, password = passwd) 
            return Response({'login': 'true', 'correo': acceso.email}, status=status.HTTP_200_OK) 
        except Evaluador.DoesNotExist: 
            return Response({'login': 'false'}, status=status.HTTP_404_NOT_FOUND) 
    
    return Response({'login': 'false'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def changePassword(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    newPassword = request.data.get('newPassword')
    passwd = passwordEncriptacion(password)
    try:
        participante = Participante.objects.get(email= email, password = passwd)
    except:
        return Response({'change': 'notSame'}, status=status.HTTP_404_NOT_FOUND) 
    
    newpasswd = passwordEncriptacion(newPassword)
    participante.password = newpasswd
    try: 
        participante.save()
        return Response({'change': 'ok'},status=status.HTTP_200_OK) 
    except: 
        return Response({'change': 'error'},status=status.HTTP_400_BAD_REQUEST) 


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def changePasswordResponsable(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    newPassword = request.data.get('newPassword')
    passwd = passwordEncriptacion(password)
    try:
        evaluador = Evaluador.objects.get(email= email, password = passwd)
    except:
        return Response({'change': 'notSame'}, status=status.HTTP_404_NOT_FOUND) 
    
    newpasswd = passwordEncriptacion(newPassword)
    evaluador.password = newpasswd
    try: 
        evaluador.save()
        return Response({'change': 'ok'},status=status.HTTP_200_OK) 
    except: 
        return Response({'change': 'error'},status=status.HTTP_400_BAD_REQUEST) 


