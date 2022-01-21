from django.http import JsonResponse
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
    
    participanteModificado = request.data.get('participante')
    participante.nombre = participanteModificado['nombre']
    participante.apellido = participanteModificado['apellido']
    participante.telefono = participanteModificado['telefono']
    participante.pais = participanteModificado['pais']
    participante.ciudad = participanteModificado['ciudad']
    participante.direccion = participanteModificado['direccion']
    participante.carreraUniversitaria = participanteModificado['carreraUniversitaria']
    participante.estudiosPrevios = participanteModificado['estudiosPrevios']
    participante.codigoEstudiante = participanteModificado['codigoEstudiante']
    participante.estadoCivil = participanteModificado['estadoCivil']
    
    try:
        participante.save()
        return Response({'edit': 'ok'},status=status.HTTP_200_OK) 
    except:
        return Response({'edit': 'error'},status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def informacionActividadesParticipante(request,correo):
    try:
        participante = Participante.objects.get(email= correo)
        actividades = Actividad.objects.all().filter(ActividadDeParticipante = participante).order_by('-fechaDeActividad')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    listadoInformacionActividades = []
    try:
        for actividad in actividades: 
            ejercitario = Ejercitario.objects.get(idEjercitario = actividad.ActividadPorEjercitario.idEjercitario)
        
            informacionActividad = {
                'idActividad' : actividad.idActividad,
                'tiempoTotalResolucionEjercitario': actividad.tiempoTotalResolucionEjercitario,
                'fechaDeActividad': actividad.fechaDeActividad,
                'totalRespuestasCorrectasIngresadasParticipante': actividad.totalRespuestasCorrectasIngresadasParticipante,
                'numeroTotalDePreguntasDelEjercitario':actividad.numeroTotalDePreguntasDelEjercitario,
                'calificacionActividad': actividad.calificacionActividad,
                'ejercitario': ejercitario.nombreDeEjercitario
            }
            listadoInformacionActividades.append(informacionActividad)
        
        return JsonResponse({"actividades":listadoInformacionActividades}, status=status.HTTP_200_OK)
    except:
        return Response({'actividades': 'error'},status=status.HTTP_400_BAD_REQUEST)


