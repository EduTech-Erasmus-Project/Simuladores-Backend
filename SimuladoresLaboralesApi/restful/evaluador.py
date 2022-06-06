from ..mixins import IsExpert
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import JsonResponse
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEvaluador(request, pk):
    try:
        evaluador = Evaluador.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    evaluador_serializer = EvaluadorSerializerObjectsNOPassword(evaluador)
    return Response(evaluador_serializer.data)
'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEvaluadorCorreo(request, correo):
    try:
        evaluador = Evaluador.objects.get(email=correo)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    evaluador_serializer = EvaluadorSerializerObjectsNOPassword(evaluador)
    return Response(evaluador_serializer.data)
'''
'''
@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def eliminarCuentaResponsable(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    passwd = passwordEncriptacion(password)
    try:
        evaluador = Evaluador.objects.get(email=email, password=passwd)
    except:
        return Response({'delete': 'notPossible'}, status=status.HTTP_404_NOT_FOUND)

    evaluador.estado = 'eliminado'
    try:
        evaluador.save()
        return Response({'delete': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'delete': 'error'}, status=status.HTTP_400_BAD_REQUEST)
'''
'''
@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def editarCuentaResponsable(request):
    email = request.data.get('correo')
    try:
        evaluador = Evaluador.objects.get(email=email)
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
        return Response({'edit': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'edit': 'error'}, status=status.HTTP_400_BAD_REQUEST)
'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getParticipantesEvaluadorAceptar(request, correo):
    try:
        evaluador = Evaluador.objects.get(email=correo)
        participantes = Participante.objects.all().filter(responsable=evaluador,
                                                          aceptacionPendianteResponsable='faltaAceptacion')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        listParticipante = []
        for participante in participantes:
            participante_serializer = ParticipanteSerializerObjectsNOPassword(participante)
            listParticipante.append(participante_serializer.data)
        return JsonResponse({"participantesAceptacion": listParticipante}, status=status.HTTP_200_OK)
    except:
        return Response({'participantesAceptacion': 'error'}, status=status.HTTP_400_BAD_REQUEST)

'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getParticipantesEvaluadorAceptados(request, correo):
    try:
        evaluador = Evaluador.objects.get(email=correo)
        participantes = Participante.objects.all().filter(responsable=evaluador,
                                                          aceptacionPendianteResponsable='aceptado')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        listParticipante = []
        for participante in participantes:
            participante_serializer = ParticipanteSerializerObjectsNOPassword(participante)
            listParticipante.append(participante_serializer.data)
        return JsonResponse({"participantes": listParticipante}, status=status.HTTP_200_OK)
    except:
        return Response({'participantesAceptacion': 'error'}, status=status.HTTP_400_BAD_REQUEST)

'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def agregarParticipanteEvaluador(request, correo):
    try:
        participante = Participante.objects.get(email=correo)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        participante.aceptacionPendianteResponsable = 'aceptado'
        participante.save()
        return JsonResponse({"participantesAceptacion": 'aceptado'}, status=status.HTTP_200_OK)
    except:
        return Response({'participantesAceptacion': 'error'}, status=status.HTTP_400_BAD_REQUEST)

'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def eliminarParticipanteEvaluador(request, correo):
    try:
        participante = Participante.objects.get(email=correo)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        participante.aceptacionPendianteResponsable = 'rechazado'
        participante.save()
        return JsonResponse({"participantesAceptacion": 'aceptado'}, status=status.HTTP_200_OK)
    except:
        return Response({'participantesAceptacion': 'error'}, status=status.HTTP_400_BAD_REQUEST)
'''

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEvaluadores(request):
    try:
        evaluadores = Evaluador.objects.all()
        evaluadorList = []
        for evaluador in evaluadores:
            evaluadorJSON = {
                'nombre': evaluador.nombre,
                'apellido': evaluador.apellido,
                'correo': evaluador.email
            }
            evaluadorList.append(evaluadorJSON)

        return JsonResponse({"evaluadores": evaluadorList}, status=status.HTTP_200_OK)

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsExpert,))
def aprobarParticipante(request):
    idEvaluador = request.user.id
    idParticipante = request.data.get('idParticipante')
    razon = request.data.get('razon')
    aprobacion = request.data.get('estado')

    try:
        participante = Participante.objects.get(id=idParticipante, evaluador__usuario_id=idEvaluador)
    except:
        return Response({"status": "error", "code": "not_found_participante"}, status=status.HTTP_404_NOT_FOUND)

    if aprobacion:
        participante.aceptacionResponsable = "aprobado"
        participante.razon = ""
    else:
        if razon == "":
            return Response({"status": "error", "code": "not_found_razon"}, status=status.HTTP_400_BAD_REQUEST)

        participante.aceptacionResponsable = "rechazado"
        participante.razon = razon
    participante.save()

    return Response({"status": "ok", "code": "ok"}, status=status.HTTP_200_OK)
