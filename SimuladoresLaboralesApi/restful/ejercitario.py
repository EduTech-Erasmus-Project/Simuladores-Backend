from distutils.command.upload import upload
import os
import uuid
from turtle import title
from unicodedata import name
from urllib import response
from django.db.models import Q, Sum
from zipfile import ZipFile
from django.core.files.storage import FileSystemStorage

#from firebase_admin import storage

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from SimuladoresLaboralesApi.views import EjercitarioViewSet

#from main.settings import BASE_DIR

# from ..mixins import ValidateToken
from rest_framework.generics import RetrieveAPIView, ListAPIView
from unityREST.settings import DEBUG

from usuario.models import Participante
from usuario.views import BASE_DIR
from ..mixins import IsExpert
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from collections import Counter


''' 
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearNuevoEjercitario(request):
    # --------------Por realizar----------------
    correoParticipante = request.data.get('participante')
    correoEvaluador = request.data.get('evaluador')
    try:
        participante = Participante.objects.get(email=correoParticipante)
        evaluador = Evaluador.objects.get(email=correoEvaluador)
    except:
        print("Error en busqueda de correo en participantes o evaluadores")
        return Response(status=status.HTTP_404_NOT_FOUND)

    asignacionRegistrar = {
        'fechaAsignacion': request.data.get('fechaAsignacion'),
        'participante': participante.id,
        'evaluador': evaluador.id
    }

    asignacionRegistrar_serializer = asignacionSerializerObjects(data=asignacionRegistrar)

    if asignacionRegistrar_serializer.is_valid():
        asignacionRegistrar_serializer.save()
        return Response({"status": "registrado"}, status=status.HTTP_201_CREATED)

    return Response(asignacionRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerAsignacionDeEjercitarioDeUnParticipante(request):
    correoParticipante = request.user["email"]
    # correoParticipante = request.data.get('correo')

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
'''

# verificar metodo


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerListaDeEscenarios(request):
    correoEvaluador = request.data.get('evaluador')
    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        # asignaciones = Asignacion.objects.all().filter(evaluador=evaluadorEjer).values()
        # return JsonResponse({"asignaciones": list(asignaciones)})
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listaEjercitario(request):
    if request.method == 'GET':
        ejercitario = Ejercitario.objects.all()
        ejercitario_serializar = EjercitarioCompetenciaSerializer(
            ejercitario, many=True)
        return Response(ejercitario_serializar.data)




@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getTotalEjercitarios(request):
    try:
        ejercitarios = Ejercitario.objects.all().count()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response({"total": ejercitarios})


class CompetenciasRetrieveAPIView(ListAPIView):
    serializer_class = CompetenciaSerializer
    queryset = Competencia.objects.all()


class CompetenciaT (ListAPIView):
    serializer_class = CompetenciaTotal
    queryset = Competencia.objects.all()


class CompetenciaRetrieveAPIView(RetrieveAPIView):
    serializer_class = CompetenciaSerializer
    queryset = Competencia.objects.all()


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarEjercitario(request):
    if (request.method == 'PUT'):
        id = request.data.get('id')
        print(request.data)

    try:
        ejercitario = Ejercitario.objects.get(id=id)

    except:
        return Response({'edit': 'notPossible'}, status=status.HTTP_404_NOT_FOUND)

    ejercitario.nombreDeEjercitario = request.data.get('nombreDeEjercitario')
    ejercitario.categoria = request.data.get('categoria')
    ejercitario.tipoDeEjercitario = request.data.get('tipoDeEjercitario')
    ejercitario.duracion = int(request.data.get('duracion'))
    ejercitario.sector = request.data.get('sector')
    ejercitario.nivel = request.data.get('nivel')
    ejercitario.competencia_id = request.data.get('competencia')
    ejercitario.urlEjercitario = request.data.get('urlEjercitario') 
    ejercitario.instruccionPrincipalEjercitario = request.data.get(
        'instruccionPrincipalEjercitario')
    ejercitario.instruccionesParticipantes = request.data.get(
        'instruccionesParticipantes')
    ejercitario.variaciones = request.data.get('variaciones')
    try:
        ejercitario.save()
        return Response({'edit': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'edit': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registroEjercitario(request):

    file = request.FILES.get('file')
    name = str(file.name)
    filename = name.split('.')[0]
    nombreDeEjercitario = request.data.get('nombreDeEjercitario')
    categoria = request.data.get('categoria')
    tipoDeEjercitario = request.data.get('tipoDeEjercitario')
    duracion = int(request.data.get('duracion'))
    sector = request.data.get('sector')
    nivel = request.data.get('nivel')
    competencia = request.data.get('competencia')
    instruccionPrincipalEjercitario = request.data.get(
        'instruccionPrincipalEjercitario')
    instruccionesParticipantes = request.data.get('instruccionesParticipantes')
    variaciones = request.data.get('variaciones')

    fss = FileSystemStorage()
    print(BASE_DIR, request._current_scheme_host)
    file = fss.save(BASE_DIR/'media'/name, file)

    with ZipFile(BASE_DIR/'media'/name) as zip:
        auxname = zip.filelist[0].filename.split('/')
        filename = f'{hex(uuid.getnode())}'
        zip.extractall(BASE_DIR/'media'/filename)
    fss.delete(file)

    preview_adapted = os.path.join(
        request._current_scheme_host, f'media/{filename}/web', 'index.html').replace("\\", "/")

    if not DEBUG:
        preview_adapted = preview_adapted.replace("http://", "https://")

    ejercitario = Ejercitario()
    ejercitario.categoria = categoria
    ejercitario.urlEjercitario = preview_adapted
    ejercitario.nombreDeEjercitario = nombreDeEjercitario
    ejercitario.tipoDeEjercitario = tipoDeEjercitario
    ejercitario.duracion = duracion
    ejercitario.sector = sector
    ejercitario.nivel = nivel
    ejercitario.competencia_id = competencia
    ejercitario.instruccionesParticipantes = instruccionesParticipantes
    ejercitario.instruccionPrincipalEjercitario = instruccionPrincipalEjercitario
    ejercitario.variaciones = variaciones

    try:
        ejercitario.save()
        return Response({'registro': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'registro': 'error'}, status=status.HTTP_400_BAD_REQUEST)

       # fss = FileSystemStorage()
    # file = fss.save(BASE_DIR/'files'/nombreDeEjercitario, file)

    # with ZipFile(BASE_DIR/'files'/nombreDeEjercitario)as zip:
    #     zip.extractall(BASE_DIR/'files')


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def recuperarEjercitario(request, pk=None):
    if request.method == 'GET':
        ejercitario = Ejercitario.objects.get(id=pk)
        ejercitarioCompetencia_serializer = EjercitarioCompetenciaSerializer(
            ejercitario)
        return Response(ejercitarioCompetencia_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registroCompetencia(request):
    competencia_serializer = CompetenciaTotal(data=request.data)
    if competencia_serializer.is_valid():
        competencia_serializer.save()
        return Response(competencia_serializer.data)
    return Response(competencia_serializer.errors)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEscenario(request, pk):
    try:
        escenario = Ejercitario.objects.get(idEjercitario=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    escenario_serializer = EjercitarioSerializerObjects(escenario)
    return Response(escenario_serializer.data)


@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEscenarioPorNumero(request, numeroDeEjercitario):
    try:
        escenario = Ejercitario.objects.get(pk=numeroDeEjercitario)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    escenario_serializer = EjercitarioSerializerObjects(escenario)
    return Response(escenario_serializer.data)


'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def crearGraficaInicioExpertoTipoDiscapacidadVsNota(request):
    correoEvaluador = request.data.get('evaluador')
    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        participantes = Participante.objects.all().filter(responsable=evaluadorEjer)
        ListaParticipantediscapacidad = []
        for p in participantes:
            discapacidadPorParticipante = DiscapacidadParticipante.objects.all().filter(participante=p)

            for discap in discapacidadPorParticipante:
                actividadParticipante = Actividad.objects.all().filter(ActividadDeParticipante=discap.participante.id)

                diccionarioConParticipantes = {

                    'participante': discap.participante.id,
                    'participanteGenero': discap.participante.genero,
                    'discapacidad': discap.discapacidad.idDiscapacidad,
                    'tipoDiscapacidad': discap.discapacidad.tipoDiscapacidad
                }

                listadoCalificaciones = []
                contCalificaciones = 0
                contCalificacionesTiempo = 0
                contnumeroActi = 0
                for actiPart in actividadParticipante:
                    contCalificaciones = contCalificaciones + actiPart.calificacionActividad
                    contCalificacionesTiempo = contCalificacionesTiempo + actiPart.tiempoTotalResolucionEjercitario
                    contnumeroActi = contnumeroActi + 1

                if (contnumeroActi > 0):
                    diccionarioConParticipantesDict = {
                        'calificacion': (contCalificaciones / contnumeroActi),
                        'tiempo': (contCalificacionesTiempo / contnumeroActi)
                    }
                    listadoCalificaciones.append(diccionarioConParticipantesDict)
                else:
                    diccionarioConParticipantesDict = {
                        'calificacion': 0,
                        'tiempo': 0
                    }
                    listadoCalificaciones.append(diccionarioConParticipantesDict)
                diccionarioConParticipantes['calificaciones'] = listadoCalificaciones

                ListaParticipantediscapacidad.append(diccionarioConParticipantes)

        return JsonResponse({"participantes": ListaParticipantediscapacidad}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
'''
'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficaInformacionGeneralTipoDiscapacidadVsNotaGeneral(request):
    # correoEvaluador = request.data.get('evaluador')
    # generoParaGrafica = request.data.get('generoParaGrafica')
    # discapacidadParaGrafica=request.data.get('discapacidadParaGrafica')
    participante = request.data.get('participante')
    listaNotaPorEvaluador = []
    try:
        actividadParticipante = Actividad.objects.all().filter(ActividadDeParticipante=participante)

        for actiPart in actividadParticipante:
            diccionarioConParticipantesNotas = {

                'calificacionActividad': actiPart.calificacionActividad
            }
            listaNotaPorEvaluador.append(diccionarioConParticipantesNotas)

        return JsonResponse({"notaGeneral": listaNotaPorEvaluador}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
'''


@api_view(['GET'])
@permission_classes((IsExpert,))
def obtenerTipoGeneroPorEvaluador(request):
    idEvaluador = request.user.id
    participantes = Usuario.objects.filter(usuario_participante__evaluador__usuario_id=idEvaluador,
                                           usuario_participante__aceptacionResponsable="aprobado")
    ListaParticipanteGenero = []
    for participante in participantes:
        ListaParticipanteGenero.append(str(participante.genero))
    counter = Counter(ListaParticipanteGenero)
    listaGeneroEvaludor = [{key: value} for key, value in counter.items()]
    return JsonResponse({"participanteGenero": listaGeneroEvaludor}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsExpert,))  # permiso sin token
def obtenerDiscapacidadesPorEvaluador(request):
    idEvaluador = request.user.id
    # print(idEvaluador)
    # TipoDiscapacidad__participante__aceptacionPendianteResponsable="aprobado"
    discapacidades = Discapacidad.objects.filter(TipoDiscapacidad__participante__evaluador__usuario_id=idEvaluador,
                                                 TipoDiscapacidad__participante__aceptacionResponsable="aprobado")
    # print("discapacidades", discapacidades)
    ListaParticipanteGenero = []
    for dicapacidad in discapacidades:
        ListaParticipanteGenero.append(str(dicapacidad.tipoDiscapacidad))
    counter = Counter(ListaParticipanteGenero)
    listaDiscapacidadEvaludor = [{key: value}
                                 for key, value in counter.items()]
    return JsonResponse({"participanteDiscapacidad": listaDiscapacidadEvaludor}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsExpert,))  # permiso sin token
def obtenerParticipantesEjercitarioPorEvaluador(request):
    idEvaluador = request.user.id
    # ejercitarios = Ejercitario.objects.filter(AsignacionEjercitario__evaluador__usuario_id=idEvaluador, AsignacionEjercitario__participante__aceptacionResponsable="aprobado")

    # ejercitarios = Ejercitario.objects.filter(competencia__asignacion_competencia__evaluador__usuario_id=idEvaluador,
    # competencia__asignacion_competencia__participante__aceptacionResponsable="aprobado")

    actividades = Actividad.objects.filter(
        participante__evaluador__usuario_id=idEvaluador)
    competencia = Competencia.objects.filter(
        competencia_ejercitario__actividad_ejercitario__in=actividades)

    # print("ejercitario", ejercitarios)
    ListaParticipanteCompetencia = []
    for competencia in competencia:
        ListaParticipanteCompetencia.append(str(competencia.titulo))
    counter = Counter(ListaParticipanteCompetencia)
    listaEjercitarioEvaludor = [{key: value} for key, value in counter.items()]
    return JsonResponse({"participanteEjercitario": listaEjercitarioEvaludor}, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes((permissions.AllowAny,)) permiso sin token
def contarParticipantesPorEvaluador(request):
    idEvaluador = request.user.id
    participantes = Participante.objects.all().filter(evaluador__usuario_id=idEvaluador,
                                                      aceptacionResponsable="aprobado").count()
    return JsonResponse({"totalParticipantes": participantes}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def obtenerDiscapacidad(request):
    print(request)
    try:
        discapacidades = Discapacidad.objects.all().values()
        return JsonResponse({"discapacidades": list(discapacidades)}, status=status.HTTP_200_OK)
    except Exception as e:
        print("error", e)
        return Response(status=status.HTTP_404_NOT_FOUND)


'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficaInfoExpertoTipoDiscapacidadVsNotas(request):
    correoEvaluador = request.data.get('evaluador')
    numeroEjercitario = request.data.get('numeroEjercitario')

    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        participantes = Participante.objects.all().filter(responsable=evaluadorEjer)
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroEjercitario)

        ListaParticipantediscapacidad = []
        for p in participantes:
            discapacidadPorParticipante = DiscapacidadParticipante.objects.all().filter(participante=p)

            for discap in discapacidadPorParticipante:
                actividadParticipante = Actividad.objects.all().filter(
                    ActividadDeParticipante=discap.participante.id).filter(ActividadPorEjercitario=ejercitario)

                if (len(actividadParticipante) > 0):

                    diccionarioConParticipantes = {
                        'ejercitario': ejercitario.numeroDeEjercitario,
                        'participante': discap.participante.id,
                        'participanteGenero': discap.participante.genero,
                        'discapacidad': discap.discapacidad.idDiscapacidad,
                        'tipoDiscapacidad': discap.discapacidad.tipoDiscapacidad
                    }

                    listadoCalificaciones = []
                    contCalificaciones = 0
                    contCalificacionesTiempo = 0
                    contnumeroActi = 0
                    for actiPart in actividadParticipante:
                        contCalificaciones = contCalificaciones + actiPart.calificacionActividad
                        contCalificacionesTiempo = contCalificacionesTiempo + actiPart.tiempoTotalResolucionEjercitario
                        contnumeroActi = contnumeroActi + 1

                    if (contnumeroActi > 0):
                        diccionarioConParticipantesDict = {
                            'calificacion': (contCalificaciones / contnumeroActi),
                            'tiempo': (contCalificacionesTiempo / contnumeroActi)
                        }
                        listadoCalificaciones.append(diccionarioConParticipantesDict)
                    else:
                        diccionarioConParticipantesDict = {
                            'calificacion': 0,
                            'tiempo': 0
                        }
                        listadoCalificaciones.append(diccionarioConParticipantesDict)
                    diccionarioConParticipantes['calificaciones'] = listadoCalificaciones

                    ListaParticipantediscapacidad.append(diccionarioConParticipantes)

        return JsonResponse({"participantes": ListaParticipantediscapacidad}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
'''
'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficaPastelGeneroPorEjercitario(request):
    correoEvaluador = request.data.get('evaluador')
    numeroEjercitario = request.data.get('numeroEjercitario')

    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        participantes = Participante.objects.all().filter(responsable=evaluadorEjer)
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroEjercitario)
        actividadParticipante = Actividad.objects.all().filter(ActividadPorEjercitario=ejercitario)
        contMujer = 0
        contHombre = 0
        contLGBT = 0
        contOtros = 0

        for actPar in actividadParticipante:
            for participante in participantes:
                if ((actPar.ActividadDeParticipante.id == participante.id) and (participante.genero == 'Mujeres')):
                    contMujer = contMujer + 1
                if ((actPar.ActividadDeParticipante.id == participante.id) and (participante.genero == 'Hombres')):
                    contHombre = contHombre + 1
                if ((actPar.ActividadDeParticipante.id == participante.id) and (participante.genero == 'LGBT')):
                    contLGBT = contLGBT + 1
                if ((actPar.ActividadDeParticipante.id == participante.id) and (participante.genero == 'Otros')):
                    contOtros = contOtros + 1

        generosSeresHumanos = [contHombre, contMujer, contLGBT, contOtros]

        return JsonResponse({"participantes": generosSeresHumanos}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
'''
'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def graficainfoParticipanteIntentosVsNotasTiempo(request):
    correoEvaluador = request.data.get('evaluador')
    numeroEjercitario = request.data.get('numeroEjercitario')
    participante = request.data.get('participante')

    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        participanteUno = Participante.objects.all().filter(id=participante)
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=numeroEjercitario)
        actividadParticipante = Actividad.objects.all().filter(ActividadPorEjercitario=ejercitario)
        listadoCalificaciones = []
        for actp in actividadParticipante:
            diccionarioConParticipantesDict = {
                'participante': actp.ActividadDeParticipante,
                'nota': actp.calificacionActividad
            }
            listadoCalificaciones.append(diccionarioConParticipantesDict)

        return JsonResponse({"participantes": listadoCalificaciones}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
'''
'''
@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
@permission_classes((IsExpert,))
def getEstudiantesEjercitarioResponsable(request, ejercitario):
    # print("ejercitario", ejercitario)
    responsable = request.user.id
    # print("ejercitario", ejercitario)
    try:
        escenario = Ejercitario.objects.get(pk=ejercitario)
        responsable = Evaluador.objects.get(usuario_id=responsable)
        asignaciones = Asignacion.objects.filter(evaluador=responsable, competencia__Competencia__id=escenario.id)
        # print("asignaciones", asignaciones)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    participantesList = []
    for asignacion in asignaciones:
        cont = 0
        if (participantesList == []):
            participantesList.append(asignacion.participante)
        else:
            for participante in participantesList:
                if (participante.id == asignacion.participante.id):
                    cont = cont + 1
            if (cont == 0):
                participantesList.append(asignacion.participante)
    # print("participantesList", participantesList)
    participantesListEjercitarioEvaluador = []
    try:
        for participante in participantesList:
            participante_serializer = ParticipanteSerializer(participante)
            participantesListEjercitarioEvaluador.append(participante_serializer.data)

        return JsonResponse({"participantes": participantesListEjercitarioEvaluador}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
'''

# metodo ligado con getEstudiantesEjercitarioResponsable


@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getNotasEstudianteEjercitarioResponsable(request, ejercitario, idParticipante):
    try:
        evaluadorEjer = request.user.id
        print(ejercitario)
        print(idParticipante)
        participante = Participante.objects.get(pk=idParticipante)
        ejercitarioAct = Ejercitario.objects.get(pk=ejercitario)

        actividadParticipante = Actividad.objects.filter(ActividadPorEjercitario=ejercitarioAct,
                                                         ActividadDeParticipante=participante,
                                                         ejercitario__AsignacionEjercitario__evaluador__usuario_id=evaluadorEjer)

        listadoCalificaciones = []
        contCalificaciones = 0
        contCalificacionesTiempo = 0
        contnumeroActi = 0
        for actiPart in actividadParticipante:
            contCalificaciones = contCalificaciones + actiPart.calificacionActividad
            contCalificacionesTiempo = contCalificacionesTiempo + \
                actiPart.tiempoTotalResolucionEjercitario
            contnumeroActi = contnumeroActi + 1

        if (contnumeroActi > 0):
            diccionarioConParticipantesDict = {
                'participante': participante.id,
                'ejercitario': ejercitarioAct.idEjercitario,
                'calificacion': round((contCalificaciones / contnumeroActi), 2),
                'tiempo': round((contCalificacionesTiempo / contnumeroActi), 2)
            }
            listadoCalificaciones.append(diccionarioConParticipantesDict)
        else:
            diccionarioConParticipantesDict = {
                'participante': participante.id,
                'ejercitario': ejercitarioAct.idEjercitario,
                'calificacion': 0,
                'tiempo': 0
            }
            listadoCalificaciones.append(diccionarioConParticipantesDict)

        return JsonResponse({"notas": listadoCalificaciones}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({"notas": []}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerInformacionLandingPage(request):
    try:
        evaluadoresCount = Evaluador.objects.all().count()
        participanteCount = Participante.objects.all().filter(estado='activo').count()
        simuladoresCount = Ejercitario.objects.all().count()

        diccionarioLandingPageDict = {
            'evaluadoresCount': evaluadoresCount,
            'participanteCount': participanteCount,
            'simuladoresCount': simuladoresCount
        }
        return Response(diccionarioLandingPageDict, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ParticipantesEjercitario(ListAPIView):
    serializer_class = UsuarioCalificacionGlobalSerializer
    permission_classes = (IsExpert,)

    def get_queryset(self):
        user = self.request.user
        ejercitarios = Ejercitario.objects.filter(
            competencia_id=self.kwargs['pk'])
        users = Usuario.objects.filter(
            usuario_participante__evaluador__usuario_id=user.id)
        users = users.filter(
            usuario_participante__actividad_participante__ejercitario_id__in=ejercitarios)
        data = []
        for user in users:
            if user not in data:
                data.append(user)

        return data


class ParticipantesPendientesListApiView(ListAPIView):
    serializer_class = ParticipanteSerializerList
    permission_classes = (IsExpert,)

    def get_queryset(self):
        user = self.request.user
        return Participante.objects.filter(evaluador__usuario_id=user.id, aceptacionResponsable="pendiente")


class ParticipantesRechazadosListApiView(ListAPIView):
    serializer_class = ParticipanteSerializerList
    permission_classes = (IsExpert,)

    def get_queryset(self):
        user = self.request.user
        return Participante.objects.filter(evaluador__usuario_id=user.id, aceptacionResponsable="rechazado")


class ParticipantesListApiView(ListAPIView):
    serializer_class = ParticipanteSerializerList
    permission_classes = (IsExpert,)

    def get_queryset(self):
        user = self.request.user
        data = Participante.objects.filter(
            evaluador__usuario_id=user.id, aceptacionResponsable="aprobado")
        print("users", data)

        return data


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def informacionCount(request):
    try:
        usuarios = Participante.objects.all().count()
        ejercitarios = Ejercitario.objects.all().count()
        competencias = Competencia.objects.all().count()
        expertos = Evaluador.objects.all().count()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response({
        "usuarios": usuarios,
        "ejercitarios": ejercitarios,
        "expertos": expertos,
        "competencias": competencias
    }, status=status.HTTP_200_OK)
