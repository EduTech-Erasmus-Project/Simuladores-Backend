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