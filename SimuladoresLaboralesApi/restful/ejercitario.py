from django.db.models import Q, Sum

from ..mixins import ValidateToken
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from collections import Counter


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


# verificar metodo
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerListaDeEscenarios(request):
    correoEvaluador = request.data.get('evaluador')
    try:
        evaluadorEjer = Evaluador.objects.get(email=correoEvaluador)
        asignaciones = Asignacion.objects.all().filter(evaluador=evaluadorEjer).values()
        return JsonResponse({"asignaciones": list(asignaciones)})
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getEscenarios(request):
    try:
        escenarios = Ejercitario.objects.all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    ejercitarios = []
    for escenario in escenarios:
        informacionEscenario = {
            'name': escenario.nombreDeEjercitario,
            'value': escenario.numeroDeEjercitario,
        }
        ejercitarios.append(informacionEscenario)
    return Response(ejercitarios)


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
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEscenarioPorNumero(request, numeroDeEjercitario):
    try:
        escenario = Ejercitario.objects.get(numeroDeEjercitario=numeroDeEjercitario)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    escenario_serializer = EjercitarioSerializerObjects(escenario)
    return Response(escenario_serializer.data)


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


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,)) permiso sin token
def obtenerTipoGeneroPorEvaluador(request):
    idEvaluador = request.user["id"]
    participantes = Participante.objects.filter(responsable__id=idEvaluador, aceptacionPendianteResponsable="aprobado")
    ListaParticipanteGenero = []
    for participante in participantes:
        ListaParticipanteGenero.append(str(participante.genero))
    counter = Counter(ListaParticipanteGenero)
    listaGeneroEvaludor = [{key: value} for key, value in counter.items()]
    return JsonResponse({"participanteGenero": listaGeneroEvaludor}, status=status.HTTP_200_OK)


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,)) permiso sin token
def obtenerDiscapacidadesPorEvaluador(request):
    idEvaluador = request.user["id"]
    print(idEvaluador)
    discapacidades = Discapacidad.objects.filter(TipoDiscapacidad__participante__responsable_id=idEvaluador, TipoDiscapacidad__participante__aceptacionPendianteResponsable="aprobado")
    ListaParticipanteGenero = []
    for dicapacidad in discapacidades:
        ListaParticipanteGenero.append(str(dicapacidad.tipoDiscapacidad))
    counter = Counter(ListaParticipanteGenero)
    listaDiscapacidadEvaludor = [{key: value} for key, value in counter.items()]
    return JsonResponse({"participanteDiscapacidad": listaDiscapacidadEvaludor}, status=status.HTTP_200_OK)


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,)) permiso sin token
def obtenerParticipantesEjercitarioPorEvaluador(request):
    idEvaluador = request.user["id"]
    ejercitarios = Ejercitario.objects.filter(AsignacionEjercitario__evaluador__id=idEvaluador, AsignacionEjercitario__participante__aceptacionPendianteResponsable="aprobado")
    ListaParticipanteEjercitario = []
    for ejercitario in ejercitarios:
        ListaParticipanteEjercitario.append(str(ejercitario.nombreDeEjercitario))
    counter = Counter(ListaParticipanteEjercitario)
    listaEjercitarioEvaludor = [{key: value} for key, value in counter.items()]
    return JsonResponse({"participanteEjercitario": listaEjercitarioEvaludor}, status=status.HTTP_200_OK)


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,)) permiso sin token
def contarParticipantesPorEvaluador(request):
    idEvaluador = request.user["id"]
    participantes = Participante.objects.all().filter(responsable__id=idEvaluador, aceptacionPendianteResponsable="aprobado").count()
    return JsonResponse({"totalParticipantes": participantes}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def obtenerDiscapacidad(request):
    try:
        discapacidades = Discapacidad.objects.all().values()
        return JsonResponse({"discapacidades": list(discapacidades)}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


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


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEstudiantesEjercitarioResponsable(request, ejercitario):
    responsable = request.user["id"]
    print(ejercitario)
    try:
        escenario = Ejercitario.objects.get(numeroDeEjercitario=ejercitario)
        responsable = Evaluador.objects.get(id=responsable)
        asignaciones = Asignacion.objects.filter(evaluador=responsable).filter(ejercitario=escenario)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
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

    participantesListEjercitarioEvaluador = []
    try:
        for participante in participantesList:
            participante_serializer = ParticipanteSerializerObjectsNOPassword(participante)
            participantesListEjercitarioEvaluador.append(participante_serializer.data)

        return JsonResponse({"participantes": participantesListEjercitarioEvaluador}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


#metodo ligado con getEstudiantesEjercitarioResponsable
@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getNotasEstudianteEjercitarioResponsable(request, ejercitario, correoParticipante):
    try:
        #evaluadorEjer = request.user["id"]
        print(ejercitario)
        print(correoParticipante)
        participante = Participante.objects.get(email=correoParticipante)
        ejercitarioAct = Ejercitario.objects.get(numeroDeEjercitario=ejercitario)
        actividadParticipante = Actividad.objects.all().filter(ActividadPorEjercitario=ejercitarioAct).filter(
            ActividadDeParticipante=participante)
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

        return JsonResponse({"notas": listadoCalificaciones}, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


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
        return Response(status=status.HTTP_404_NOT_FOUND)
