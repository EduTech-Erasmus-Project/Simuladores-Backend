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
from django.http import JsonResponse
import datetime
import statistics

''' 
#verificar metodo
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearNuevaAsignacion(request): 
    correoParticipante = request.data.get('participante')
    correoEvaluador = request.data.get('evaluador')
    numeroejercitario = request.data.get('ejercitario')

    try: 
        participante = Participante.objects.get(email=correoParticipante) 
        evaluador = Evaluador.objects.get(email=correoEvaluador)  
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroejercitario)  
    except: 
        print("Error en busqueda de correo en participantes o evaluadores")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    asignacionRegistrar = {
        'fechaAsignacion' : request.data.get('fechaAsignacion'),
        'participante' : participante.id,
        'evaluador' : evaluador.id,
        'ejercitario' : ejercitario.idEjercitario
    }
    
    asignacionRegistrar_serializer = asignacionSerializerObjects(data=asignacionRegistrar)
    
    if asignacionRegistrar_serializer.is_valid():
        asignacionRegistrar_serializer.save()
        return Response({"status": "registrado"}, status=status.HTTP_201_CREATED) 
    
    return Response(asignacionRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''

'''
#verificar metodo
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def agregarAsignacioneParticipante(request): 
    correoParticipante = request.data.get('emailParticipanteSeleccion')
    correoEvaluador = request.data.get('correoEvaluadorActividades')
    numeroejercitario = request.data.get('selectedEjercitario')
    fecha = request.data.get('fechaActividad')

    try: 
        participante = Participante.objects.get(email=correoParticipante) 
        evaluador = Evaluador.objects.get(email=correoEvaluador)  
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroejercitario)  
    except: 
        print("Error en busqueda de correo en participantes o evaluadores")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    asignacionRegistrar = {
        'fechaAsignacion' : fecha,
        'participante' : participante.id,
        'evaluador' : evaluador.id,
        'ejercitario' : ejercitario.idEjercitario
    }
    
    asignacionRegistrar_serializer = asignacionSerializerObjects(data=asignacionRegistrar)
    
    if asignacionRegistrar_serializer.is_valid():
        asignacionRegistrar_serializer.save()
        informacionAsignacion = {
            'idAsignacion':asignacionRegistrar_serializer.data['idAsignacion'],
            'fechaAsignacion':  fecha,
            'participante': participante.email,
            'evaluador': evaluador.email,
            'numeroDeEjercitario': ejercitario.numeroDeEjercitario,
            'nombreDeEjercitario': ejercitario.nombreDeEjercitario
        }
        return Response(informacionAsignacion, status=status.HTTP_201_CREATED) 
    
    return Response(asignacionRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
#verificar metod
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def tiempoTotalResolucionCompletaPorEjercitario(request): 
    generoParticipante = request.data.get('generoParticipante')
    discapacidadParticipante = request.data.get('discapacidad')
    numeroEscenario = request.data.get('NumeroEscenario')
    correoEvaluador = request.data.get('correoEvaluador')
    
    try: 
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        escenarioEjer = Ejercitario.objects.get(numeroDeEjercitario = numeroEscenario)
        asignaciones = Asignacion.objects.all().filter(evaluador= evaluadorEjer, ejercitario = escenarioEjer)
        
        discapacidadEjer = Discapacidad.objects.get(tipoDiscapacidad=discapacidadParticipante)
        discapacidadPartipantes = DiscapacidadParticipante.objects.all().filter(discapacidad = discapacidadEjer)
        participantes = Participante.objects.all().filter(responsable= evaluadorEjer, genero = generoParticipante)
        
        listParticipantesFiltrados = []
        for discapacidadPartipante in discapacidadPartipantes:
            for participante in participantes:
                if (discapacidadPartipante.participante.id == participante.id):
                    listParticipantesFiltrados.append(participante)
                   
        listParticipantesFiltradosConAsignacion = []          
        for asignacion in asignaciones:
            for participante in listParticipantesFiltrados:
                if(asignacion.participante.id == participante.id):
                    listParticipantesFiltradosConAsignacion.append(participante)
        
        listadoTiempo = []
        for participante in listParticipantesFiltradosConAsignacion:
            actividades = Actividad.objects.all().filter(ActividadDeParticipante= participante)
            for actividad in actividades: 
                
                print(actividad.tiempoInicio)
                tiempoA = actividad.tiempoInicio.split(':') 
                tiempoB = actividad.tiempoFin.split(':') 
                a = datetime.timedelta(hours=int(tiempoA[0]),minutes=int(tiempoA[1]), seconds=int(tiempoA[2]))
                b = datetime.timedelta(hours=int(tiempoB[0]),minutes=int(tiempoB[1]), seconds=int(tiempoB[2]))
                c = round((((b - a).total_seconds())),2)
                listadoTiempo.append(c)
                
        return Response({"tiempo": round((statistics.mean(listadoTiempo)/60),2)}, status=status.HTTP_201_CREATED) 
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
'''

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def eliminarAsignacion(request,idAsignacion):
    try:
        asignacion = Asignacion.objects.get(idAsignacion= idAsignacion)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    try:    
        asignacion.delete() 
        return JsonResponse({"asignacion":'delete'}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'asignacion': 'error'},status=status.HTTP_400_BAD_REQUEST)
'''