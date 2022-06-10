import os

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.template.loader import get_template
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import hashlib
import environ
import pdfkit


env = environ.Env()

@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getParticipante(request, pk):
    '''
    try:
        participante = Participante.objects.get(email= correo)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    participante_serializer = ParticipanteSerializerObjectsNOPassword(participante)
    return Response(participante_serializer.data)
    '''
    participante = get_object_or_404(Participante, pk=pk)
    serializer = ParticipanteSerializerDiscapacidad(participante)
    return Response(serializer.data, status=status.HTTP_200_OK)

''' 
def passwordEncriptacion(password):
    encoded = password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()
'''

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getParticipanteDeUnResponsable(request, correo, correoResponsable):
    try:
        evaluador = Evaluador.objects.get(email=correoResponsable)
        participante = Participante.objects.all().filter(email=correo).filter(responsable=evaluador)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    participante_serializer = ParticipanteSerializerObjectsNOPassword(participante[0])
    if participante_serializer.is_valid:
        return Response(participante_serializer.data)
    return Response(participante_serializer.errors)
'''
'''
def passwordEncriptacion(password):
    encoded = password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()
'''
'''
@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def eliminarCuentaParticipante(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    passwd = passwordEncriptacion(password)
    try:
        participante = Participante.objects.get(email=email, password=passwd)
    except:
        return Response({'delete': 'notPossible'}, status=status.HTTP_404_NOT_FOUND)

    participante.estado = 'eliminado'
    try:
        participante.save()
        return Response({'delete': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'delete': 'error'}, status=status.HTTP_400_BAD_REQUEST)
'''
'''
@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarCuentaParticipante(request):
    email = request.data.get('correo')
    try:
        participante = Participante.objects.get(email=email)
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
        return Response({'edit': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'edit': 'error'}, status=status.HTTP_400_BAD_REQUEST)

'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def informacionActividadesParticipante(request, correo):
    try:
        participante = Participante.objects.get(email=correo)
        actividades = Actividad.objects.all().filter(ActividadDeParticipante=participante).order_by('-fechaDeActividad')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    listadoInformacionActividades = []
    try:
        for actividad in actividades:
            ejercitario = Ejercitario.objects.get(idEjercitario=actividad.ActividadPorEjercitario.idEjercitario)

            informacionActividad = {
                'idActividad': actividad.idActividad,
                'tiempoTotalResolucionEjercitario': actividad.tiempoTotalResolucionEjercitario,
                'fechaDeActividad': actividad.fechaDeActividad,
                'totalRespuestasCorrectasIngresadasParticipante': actividad.totalRespuestasCorrectasIngresadasParticipante,
                'numeroTotalDePreguntasDelEjercitario': actividad.numeroTotalDePreguntasDelEjercitario,
                'calificacionActividad': actividad.calificacionActividad,
                'ejercitario': ejercitario.nombreDeEjercitario
            }
            listadoInformacionActividades.append(informacionActividad)

        return JsonResponse({"actividades": listadoInformacionActividades}, status=status.HTTP_200_OK)
    except:
        return Response({'actividades': 'error'}, status=status.HTTP_400_BAD_REQUEST)
'''

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getParticipantesIntentosEjercitario(request, correo, ejercitario):
    try:
        participante = Participante.objects.get(email=correo)
        ejercitario = Ejercitario.objects.get(numeroDeEjercitario=ejercitario)
        actividades = Actividad.objects.all().filter(ActividadDeParticipante=participante).filter(
            ActividadPorEjercitario=ejercitario).order_by('-fechaDeActividad').values()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"actividades": list(actividades)}, status=status.HTTP_200_OK)

''' 
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def obtenerInformacionAsignacionesParticipante(request, correo, correoResponsable):
    try:
        evaluadorBuscado = Evaluador.objects.get(email=correoResponsable)
        participanteBuscado = Participante.objects.get(email=correo)
        asignaciones = Asignacion.objects.all().filter(participante=participanteBuscado).filter(
            evaluador=evaluadorBuscado).order_by('-fechaAsignacion')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    listadoInformacionAsignaciones = []

    try:
        for asignacion in asignaciones:
            ejercitario = Ejercitario.objects.get(idEjercitario=asignacion.ejercitario.idEjercitario)
            informacionAsignacion = {
                'idAsignacion': asignacion.idAsignacion,
                'fechaAsignacion': asignacion.fechaAsignacion,
                'participante': participanteBuscado.email,
                'evaluador': evaluadorBuscado.email,
                'numeroDeEjercitario': ejercitario.numeroDeEjercitario,
                'nombreDeEjercitario': ejercitario.nombreDeEjercitario
            }
            listadoInformacionAsignaciones.append(informacionAsignacion)

        return JsonResponse({"asignaciones": listadoInformacionAsignaciones}, status=status.HTTP_200_OK)
    except:

        return Response({'asignaciones': 'error'}, status=status.HTTP_400_BAD_REQUEST)

'''

@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getReporte(request, idCompetencia, idParticipante):
    try:
        competencia = Competencia.objects.get(id=idCompetencia)
        usuario = Usuario.objects.get(usuario_participante=idParticipante)
        usuario_serialize = UsuarioSerializer(usuario)

        nivel1 = Actividad.objects.filter(participante_id=idParticipante, ejercitario__competencia_id=idCompetencia,
                                          ejercitario__nivel="Nivel1").order_by("-id")
        nivel2 = Actividad.objects.filter(participante_id=idParticipante, ejercitario__competencia_id=idCompetencia,
                                          ejercitario__nivel="Nivel2").order_by("-id")
        nivel3 = Actividad.objects.filter(participante_id=idParticipante, ejercitario__competencia_id=idCompetencia,
                                          ejercitario__nivel="Nivel3").order_by("-id")

        ''' 
        if len(nivel1) == 0 or len(nivel2) == 0 or len(nivel3) == 0:
            return Response({"status": "error", "code": "incomplete_grade"}, status=status.HTTP_400_BAD_REQUEST)

        if nivel1[0].calificacion != 100 or nivel2[0].calificacion != 100 or nivel3[0].calificacion != 100:
            return Response({"status": "error", "code": "incomplete_grade"}, status=status.HTTP_400_BAD_REQUEST)
        '''

        data = {
            "usuario": usuario_serialize.data,
            "competencia": {
                "id": competencia.id,
                "titulo": competencia.titulo,
                "niveles": [
                    {
                        "label": "Nivel 1",
                        "value": "Nivel1",
                        "estado": "Aprobado" if len(nivel1) > 0 and nivel1[0].calificacion == 100 else "Cursando",
                        "fecha": nivel1[0].fecha if len(nivel1) > 0 else None,
                        "calificacion": nivel1[0].calificacion if len(nivel1) > 0 else 0,
                        "intentos": len(nivel1),
                        "actividades": nivel1.values(),
                    },
                    {
                        "label": "Nivel 2",
                        "value": "Nivel2",
                        "estado": "Aprobado" if len(nivel2) > 0 and nivel2[0].calificacion == 100 else "Cursando",
                        "fecha": nivel2[0].fecha if len(nivel2) > 0 else None,
                        "calificacion": nivel2[0].calificacion if len(nivel2) > 0 else 0,
                        "intentos": len(nivel2),
                        "actividades": nivel2.values(),
                    },
                    {
                        "label": "Nivel 3",
                        "value": "Nivel3",
                        "estado": "Aprobado" if len(nivel3) > 0 and nivel3[0].calificacion == 100 else "Cursando",
                        "fecha": nivel3[0].fecha if len(nivel3) > 0 else None,
                        "calificacion": nivel3[0].calificacion if len(nivel3) > 0 else 0,
                        "intentos": len(nivel3),
                        "actividades": nivel3.values(),
                    }
                ]
            }
        }

        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"status": "error", "code": "not_found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def download_certificado(request, idCompetencia, idParticipante):
    try:
        pass
    except Exception as e:
        pass


@api_view(['GET'])
def descargar_certificado(request, idCompetencia, idParticipante):
    print(idCompetencia)
    serializer = geanarar_certificado(idCompetencia, idParticipante, request)
    return Response(serializer.data, status=status.HTTP_200_OK)




def geanarar_certificado(idCompetencia, idParticipante, request):
    competencia = Competencia.objects.get(id=idCompetencia)
    usuario = Usuario.objects.get(usuario_participante=idParticipante)
    evaluador = Usuario.objects.get(id=request.user.id)


    template = get_template('cert/certificate.html')



    # Add any context variables you need to be dynamically rendered in the HTML
    context = {}

    context["usuario"] = usuario
    context["competencia"] = competencia
    context["evaluador"] = evaluador
    # Render the HTML
    html = template.render(context)

    print(html)

    options = {
        'encoding': 'UTF-8',
        # 'javascript-delay': '1000',  # Optional
        'enable-local-file-access': None,  # To be able to access CSS
        'page-size': 'A4',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
    }

    print("path", env('wkhtmltopdf'))

    # Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdfkit.from_string(html, "file.pdf", configuration=config, options=options)
    certificado = Certificado(
        competencia=competencia,
        participante_id=idParticipante,
        #certificado=file_content
    )
    certificado.save()
    return CertificadoSerializer(certificado)



class CertificateView(TemplateView):
    template_name = 'cert/certificate.html'
