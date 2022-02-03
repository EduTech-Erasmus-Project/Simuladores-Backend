from ..models import * 
from ..serializers import * 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getDiscapacidadesDelParticipante(request,correo):
    try:
        participanteDis = Participante.objects.get(email= correo)
        discapacidades = DiscapacidadParticipante.objects.all().filter(participante = participanteDis)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    discapacidadesList = []
    for discapacidadParticipante in discapacidades:
        discapacidadInf = Discapacidad.objects.get(idDiscapacidad = discapacidadParticipante.discapacidad.idDiscapacidad)
        informacionDiscapacidad = {
            'idGradoDeDiscapacidad' : discapacidadParticipante.idGradoDeDiscapacidad,
            'gradoDeDiscapacidad': discapacidadParticipante.gradoDeDiscapacidad,
            'participante_id': discapacidadParticipante.participante_id,
            'tipoDiscapacidad': discapacidadInf.tipoDiscapacidad,
        }
        discapacidadesList.append(informacionDiscapacidad)
    
    return JsonResponse({"discapacidadesParticipante":discapacidadesList}, status=status.HTTP_200_OK)