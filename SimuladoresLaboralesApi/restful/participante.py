from ..models import * 
from ..serializers import * 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import hashlib


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getParticipante(request,correo):
    try:
        participante = Participante.objects.get(email= correo)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    participante_serializer = ParticipanteSerializerObjectsNOPassword(participante)
    return Response(participante_serializer.data)

def passwordEncriptacion(password):
    encoded=password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()

@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def eliminarCuentaParticipante(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    passwd = passwordEncriptacion(password)
    try:
        participante = Participante.objects.get(email= email, password = passwd)
    except:
        return Response({'delete': 'notPossible'}, status=status.HTTP_404_NOT_FOUND) 
    
    participante.estado = 'eliminado'
    try: 
        participante.save()
        return Response({'delete': 'ok'},status=status.HTTP_200_OK) 
    except: 
        return Response({'delete': 'error'},status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarCuentaParticipante(request):
    
    email = request.data.get('correo')
    try:
        participante = Participante.objects.get(email= email)
    except:
        return Response({'edit': 'notPossible'}, status=status.HTTP_404_NOT_FOUND) 
    
    
    
    print("********",request.data.get('participante')[0])
    print("--------",list(participante.__dict__))
    if serializer.is_valid():
       
        return Response({'edit': 'ok'},status=status.HTTP_200_OK) 
    
    return Response({'edit': 'error'},status=status.HTTP_400_BAD_REQUEST)
    """try: 
        #participante.save()
        return Response({'edit': 'ok'},status=status.HTTP_200_OK) 
    except: 
        return Response({'edit': 'error'},status=status.HTTP_400_BAD_REQUEST) """