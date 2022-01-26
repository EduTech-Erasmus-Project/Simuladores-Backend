from importlib_metadata import email
from ..models import * 
from ..serializers import * 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import hashlib

def passwordEncriptacion(password):
    encoded=password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEvaluador(request,pk):
    try:
        evaluador = Evaluador.objects.get(id= pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    evaluador_serializer = EvaluadorSerializerObjectsNOPassword(evaluador)
    return Response(evaluador_serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEvaluadorCorreo(request,correo):
    try:
        evaluador = Evaluador.objects.get(email= correo)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    evaluador_serializer = EvaluadorSerializerObjectsNOPassword(evaluador)
    return Response(evaluador_serializer.data)

@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def eliminarCuentaResponsable(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    passwd = passwordEncriptacion(password)
    try:
        evaluador = Evaluador.objects.get(email= email, password = passwd)
    except:
        return Response({'delete': 'notPossible'}, status=status.HTTP_404_NOT_FOUND) 
    
    evaluador.estado = 'eliminado'
    try: 
        evaluador.save()
        return Response({'delete': 'ok'},status=status.HTTP_200_OK) 
    except: 
        return Response({'delete': 'error'},status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarCuentaResponsable(request):
    
    email = request.data.get('correo')
    try:
        evaluador = Evaluador.objects.get(email= email)
    except:
        return Response({'edit': 'notPossible'}, status=status.HTTP_404_NOT_FOUND) 
    
    responsableModificado = request.data.get('responsable')
    evaluador.nombre = responsableModificado['nombre']
    evaluador.apellido = responsableModificado['apellido']
    evaluador.telefono = responsableModificado['telefono']
    evaluador.pais = responsableModificado['pais']
    evaluador.ciudad = responsableModificado['ciudad']
    evaluador.direccion = responsableModificado['direccion']
    evaluador.nivelDeFormacion = responsableModificado['nivelDeFormacion']
    try:
        evaluador.save()
        return Response({'edit': 'ok'},status=status.HTTP_200_OK) 
    except:
        return Response({'edit': 'error'},status=status.HTTP_400_BAD_REQUEST) 