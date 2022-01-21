import email
from typing import Counter
from urllib import request
from ..models import * 
from ..serializers import * 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from rest_framework import serializers
from django.core import serializers as core_serializers
import json
from django.http import JsonResponse

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearNuevoEjercitario(request):
    #--------------Por realizar---------------- 
    correoParticipante = request.data.get('participante')
    correoEvaluador = request.data.get('evaluador')
    try: 
        participante = Participante.objects.get(email=correoParticipante) 
        evaluador = Evaluador.objects.get(email=correoEvaluador)  
    except: 
        print("Error en busqueda de correo en participantes o evaluadores")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    asignacionRegistrar = {
        'fechaAsignacion' : request.data.get('fechaAsignacion'),
        'participante' : participante.id,
        'evaluador' : evaluador.id
    }
    
    asignacionRegistrar_serializer = asignacionSerializerObjects(data=asignacionRegistrar)
    
    if asignacionRegistrar_serializer.is_valid():
        asignacionRegistrar_serializer.save()
        return Response({"status": "registrado"}, status=status.HTTP_201_CREATED) 
    
    return Response(asignacionRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerAsignacionDeEjercitarioDeUnParticipante(request): 
    correoParticipante = request.data.get('correo')
    
    try: 
        participanteObtenido = Participante.objects.get(email=correoParticipante)
    except: 
        print("Error en busqueda de correo en participante")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    try: 
        asignaciones = Asignacion.objects.all().filter(participante=participanteObtenido).values()
    except: 
        print("Error en busqueda de Asignaciones")
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    return JsonResponse({"asignaciones": list(asignaciones)})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerListaDeEscenarios(request):

    correoEvaluador = request.data.get('evaluador')
    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        asignaciones = Asignacion.objects.all().filter(evaluador= evaluadorEjer).values()
        return JsonResponse({"asignaciones": list(asignaciones)})      
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEscenario(request,pk):
    try:
        escenario = Ejercitario.objects.get(idEjercitario= pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    escenario_serializer = EjercitarioSerializerObjects(escenario)
    return Response(escenario_serializer.data)



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearGraficaInicioExpertoTipoDiscapacidadVsNota(request):

    correoEvaluador = request.data.get('evaluador')
    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador) 
        participantes = Participante.objects.all().filter(responsable = evaluadorEjer)
        ListaParticipantediscapacidad= []
        for p in participantes:
            discapacidadPorParticipante = DiscapacidadParticipante.objects.all().filter(participante = p)

            for discap in discapacidadPorParticipante:
                actividadParticipante = Actividad.objects.all().filter(ActividadDeParticipante = discap.participante.id)
                
                
                diccionarioConParticipantes = {
                    
                        'participante' : discap.participante.id,
                        'participanteGenero' : discap.participante.genero,
                        'discapacidad' : discap.discapacidad.idDiscapacidad,
                        'tipoDiscapacidad' : discap.discapacidad.tipoDiscapacidad
                }

                listadoCalificaciones = []
                contCalificaciones = 0
                contnumeroActi = 0
                for actiPart in actividadParticipante:
                    contCalificaciones = contCalificaciones+actiPart.calificacionActividad 
                    contnumeroActi = contnumeroActi + 1
                if (contnumeroActi > 0):
                    diccionarioConParticipantesDict = {
                        'calificacion':  (contCalificaciones/contnumeroActi)
                    }
                    listadoCalificaciones.append(diccionarioConParticipantesDict)
                else:
                    diccionarioConParticipantesDict = {
                        'calificacion':  0
                    }
                    listadoCalificaciones.append(diccionarioConParticipantesDict)
                diccionarioConParticipantes['calificaciones'] = listadoCalificaciones

                ListaParticipantediscapacidad.append(diccionarioConParticipantes)

            
            
        return JsonResponse({"participantes": ListaParticipantediscapacidad}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral(request):
    #correoEvaluador = request.data.get('evaluador')
    #generoParaGrafica = request.data.get('generoParaGrafica')
    #discapacidadParaGrafica=request.data.get('discapacidadParaGrafica')
    participante = request.data.get('participante')
    listaNotaPorEvaluador = []
    try: 
        actividadParticipante = Actividad.objects.all().filter(ActividadDeParticipante = participante)

        for actiPart in actividadParticipante:
                diccionarioConParticipantesNotas = {
                    
                    'calificacionActividad' : actiPart.calificacionActividad
                }
                listaNotaPorEvaluador.append(diccionarioConParticipantesNotas)

        
        
        return JsonResponse({"notaGeneral": listaNotaPorEvaluador}, status=status.HTTP_201_CREATED)
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND) 


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficaInformacionGeneralTipoDiscapacidadVsTiempoGeneral(request):
    #correoEvaluador = request.data.get('evaluador')
    #generoParaGrafica = request.data.get('generoParaGrafica')
    #discapacidadParaGrafica=request.data.get('discapacidadParaGrafica')
    participante = request.data.get('participante')
    listaNotaPorEvaluador = []
    try: 
        actividadParticipante = Actividad.objects.all().filter(ActividadDeParticipante = participante)

        for actiPart in actividadParticipante:
                diccionarioConParticipantesNotas = {
                    
                    'calificacionActividad' : actiPart.calificacionActividad
                }
                listaNotaPorEvaluador.append(diccionarioConParticipantesNotas)

        
        
        return JsonResponse({"notaGeneral": listaNotaPorEvaluador}, status=status.HTTP_201_CREATED)
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND) 



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def obtenerTipoGeneroPorEvaluador(request):
    
    correoEvaluador = request.data.get('evaluador')
    try: 
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador) 
        
        participantes = Participante.objects.all().filter(responsable = evaluadorEjer)
        

        ListaParticipanteGenero= []
        for participante in participantes:
            ListaParticipanteGenero.append(participante.genero)
        
        print()
        listaGeneroEvaludor = list(Counter(ListaParticipanteGenero).keys())
         
        return JsonResponse({"participanteGenero": listaGeneroEvaludor}, status=status.HTTP_201_CREATED)    
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND) 


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def obtenerDiscapacidad(request):
    try: 
        discapacidades = Discapacidad.objects.all().values()
        print(discapacidades)
        return JsonResponse({"discapacidades": list(discapacidades)}, status=status.HTTP_201_CREATED)    
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND) 


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def obtenerGraficaGeneralDiscapacidadvsTiempoGeneral(request):

    participante = request.data.get('participante')

    listaTiempoGlobalPorEvaluador = []
    try: 
        actividadParticipante = Actividad.objects.all().filter(ActividadDeParticipante = participante)

        for actiPart in actividadParticipante:

            diccionarioConParticipantesTiempoGlobles = {
                    
                'calificacionActividad' : actiPart.calificacionActividad
            }
            listaTiempoGlobalPorEvaluador.append(diccionarioConParticipantesTiempoGlobles)
    
               
                
        return JsonResponse({"tiempo":listaTiempoGlobalPorEvaluador }, status=status.HTTP_201_CREATED) 
    except: 
        return Response(status=status.HTTP_404_NOT_FOUND) 