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
import datetime

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearNuevaActividadUnity2(request): 
    print("**********", request.data)
    tiempoInicio = request.data.get('tiempoInicio')
    tiempoFin = request.data.get('tiempoFin')
    fechaDeActividad = request.data.get('fechaDeActividad')
    
    #fecha_dt = datetime.strptime(request.data.get('fechaDeActividad'), '%d/%m/%Y %HH%')
    #print(fecha_dt)
    
    numeroEjercitario = request.data.get('numeroEjercitario')
    correo = request.data.get('correo')
    try: 
        participante = Participante.objects.get(email=correo) 
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroEjercitario)  
    except: 
        print("Error en busqueda de correo en participantes o evaluadores")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    nuevaActividadRegistrar = {
        'tiempoInicio' : tiempoInicio,
        'tiempoFin' : tiempoFin,
        'fechaDeActividad' : fechaDeActividad,
        'ActividadPorEjercitario' : ejercitario.idEjercitario,
        'ActividadDeParticipante' : participante.id
    }
    
    nuevaActividadUnity_serializer = nuevaActividadUnitySerializerObjects(data=nuevaActividadRegistrar)
    
    if nuevaActividadUnity_serializer.is_valid():
        nuevaActividadUnity_serializer.save()
        try:
            
            actividad = Actividad.objects.order_by('-idActividad')[0]
            preguntas = request.data.get('preguntas')
            for pregunta in preguntas:
                nuevaPreguntaRegistrar = {
                    'numeroPregunta' : pregunta['numeroPregunta'],
                    'respuestaIngresada': pregunta['respuestaIngresada'],
                    'tiempoRespuesta': pregunta['tiempoRespuesta'],
                    'preguntaDeLaActividad' : actividad.idActividad
                }
                
                nuevaPreguntaUnity_serializer = nuevaPreguntaUnitySerializerObjects(data=nuevaPreguntaRegistrar)
                print(nuevaPreguntaUnity_serializer.is_valid())
                if nuevaPreguntaUnity_serializer.is_valid():
                    nuevaPreguntaUnity_serializer.save()
                else:
                    return Response(nuevaPreguntaUnity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({"status": "actividad registrada"}, status=status.HTTP_201_CREATED) 
        
        except Actividad.DoesNotExist: 
            return Response({'Actividad': 'noExist'}, status=status.HTTP_404_NOT_FOUND) 
        
        
    
    return Response(nuevaActividadUnity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearNuevaActividadUnity(request): 
    print("**********", request.data)
    tiempoInicio = request.data.get('tiempoInicio')
    tiempoFin = request.data.get('tiempoFin')
    fechaDeActividad = request.data.get('fechaDeActividad')
    
    #fecha_dt = datetime.strptime(request.data.get('fechaDeActividad'), '%d/%m/%Y %HH%')
    #print(fecha_dt)
    
    numeroEjercitario = request.data.get('numeroEjercitario')
    correo = request.data.get('correo')
    try: 
        participante = Participante.objects.get(email=correo) 
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroEjercitario) 
        preguntasEjercitario =  Pregunta.objects.all().filter(preguntaDelEjercitario = ejercitario)
    except: 
        print("Error en busqueda de correo en participantes o evaluadores")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    tiempoA = tiempoInicio.split(':') 
    tiempoB = tiempoFin.split(':') 
    a = datetime.timedelta(hours=int(tiempoA[0]),minutes=int(tiempoA[1]), seconds=int(tiempoA[2]))
    b = datetime.timedelta(hours=int(tiempoB[0]),minutes=int(tiempoB[1]), seconds=int(tiempoB[2]))
    tiempoTotalResolucionEjercitario = round((((b - a).total_seconds())),2)
    
    
    nuevaActividadRegistrar = {
        'tiempoInicio' : tiempoInicio,
        'tiempoFin' : tiempoFin,
        'fechaDeActividad' : fechaDeActividad,
        'tiempoTotalResolucionEjercitario':tiempoTotalResolucionEjercitario,
        'ActividadPorEjercitario' : ejercitario.idEjercitario,
        'ActividadDeParticipante' : participante.id
    }
    
    nuevaActividadUnity_serializer = nuevaActividadUnitySerializerObjects(data=nuevaActividadRegistrar)
    
    if nuevaActividadUnity_serializer.is_valid():
        nuevaActividadUnity_serializer.save()
        try:
            
            actividad = Actividad.objects.order_by('-idActividad')[0]
            preguntas = request.data.get('preguntas')
            cont = 0
            totalPreguntas = 0
            for pregunta in preguntas:
                for preguntasRespuesta in preguntasEjercitario:
                    if(preguntasRespuesta.numeroPregunta == pregunta['numeroPregunta']):
                        if(preguntasRespuesta.respuestaCorrecta == pregunta['respuestaIngresada']):
                            cont = cont + 1
                            totalPreguntas = totalPreguntas +1
                        else: 
                            totalPreguntas = totalPreguntas +1
                nuevaPreguntaRegistrar = {
                    'numeroPregunta' : pregunta['numeroPregunta'],
                    'respuestaIngresada': pregunta['respuestaIngresada'],
                    'tiempoRespuesta': pregunta['tiempoRespuesta'],
                    'preguntaDeLaActividad' : actividad.idActividad
                }
                
                nuevaPreguntaUnity_serializer = nuevaPreguntaUnitySerializerObjects(data=nuevaPreguntaRegistrar)
                print(nuevaPreguntaUnity_serializer.is_valid())
                if nuevaPreguntaUnity_serializer.is_valid():
                    nuevaPreguntaUnity_serializer.save()
                else:
                    return Response(nuevaPreguntaUnity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #Almacenamiento de calificaciones  
            actividad.totalRespuestasCorrectasIngresadasParticipante = cont
            actividad.numeroTotalDeRespuestasContestadasPorElParticipante = totalPreguntas
            actividad.numeroTotalDePreguntasDelEjercitario = len(preguntasEjercitario)
            actividad.calificacionActividad = ( cont*100/len(preguntasEjercitario))
            actividad.save()
            
            return Response({"status": "actividad registrada"}, status=status.HTTP_201_CREATED) 
        
        except Actividad.DoesNotExist: 
            return Response({'Actividad': 'noExist'}, status=status.HTTP_404_NOT_FOUND) 
        
        
    
    return Response(nuevaActividadUnity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)