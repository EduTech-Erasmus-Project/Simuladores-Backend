from rest_framework.generics import  ListAPIView

from ..mixins import IsAdmin
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getDiscapacidadesDelParticipante(request, correo):
    try:
        participanteDis = Participante.objects.get(email=correo)
        discapacidades = DiscapacidadParticipante.objects.all().filter(participante=participanteDis)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    discapacidadesList = []
    for discapacidadParticipante in discapacidades:
        discapacidadInf = Discapacidad.objects.get(idDiscapacidad=discapacidadParticipante.discapacidad.idDiscapacidad)
        informacionDiscapacidad = {
            'idGradoDeDiscapacidad': discapacidadParticipante.idGradoDeDiscapacidad,
            'gradoDeDiscapacidad': discapacidadParticipante.gradoDeDiscapacidad,
            'participante_id': discapacidadParticipante.participante_id,
            'tipoDiscapacidad': discapacidadInf.tipoDiscapacidad,
        }
        discapacidadesList.append(informacionDiscapacidad)

    return JsonResponse({"discapacidadesParticipante": discapacidadesList}, status=status.HTTP_200_OK)
'''
'''
# admin role
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registrarDiscapacidad(request):
    discapacidad = request.data.get('discapacidad')
    porcentaje = request.data.get('porcentaje')
    correo = request.data.get('correo')
    try:
        discapacidadSeleccionada = Discapacidad.objects.get(tipoDiscapacidad=discapacidad)
        participanteSeleccionado = Participante.objects.get(email=correo)
    except Discapacidad.DoesNotExist:
        return Response({'discapacidad': 'noExist'}, status=status.HTTP_404_NOT_FOUND)

    discapacidadRegistrar = {
        'gradoDeDiscapacidad': porcentaje,
        'participante': participanteSeleccionado.id,
        'discapacidad': discapacidadSeleccionada.idDiscapacidad,
    }

    discapacidadRegistrar_serializer = DiscapacidadParticipanteSerializerObjects(data=discapacidadRegistrar)
    if discapacidadRegistrar_serializer.is_valid():
        discapacidadRegistrar_serializer.save()

        return Response({"status": "discapacidad registrada"}, status=status.HTTP_201_CREATED) 
    
    return Response(discapacidadRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getDiscapacidad(request):
    if request.method == 'GET':
        discapacidad = Discapacidad.objects.all()
        discapacidad_serializer = DiscapacidadSerializer(discapacidad, many =True)
        return Response(discapacidad_serializer.data)

class discapacidadTotal (ListAPIView):
    serializer_class = DiscapacidadSerializer
    queryset = Discapacidad.objects.all()


@api_view(['POST'])
@permission_classes((IsAdmin,))
def regiDiscapacidad(request):
    discapacidad_serializer = DiscapacidadSerializer(data=request.data)
    if discapacidad_serializer.is_valid():
        discapacidad_serializer.save()
        return Response(discapacidad_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(discapacidad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def editarDiscapacidad(request,pk=None):
    discapacidad = Discapacidad.objects.get(id=pk)
    discapacidad_serializer = DiscapacidadSerializer(discapacidad)
    return Response(discapacidad_serializer.data, status=status.HTTP_200_OK)
