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
def getExperienciaLaboral(request,correo):
    try:
        participanteEXP = Participante.objects.get(email= correo)
        experienciasPartipante = ExperienciaLaboral.objects.all().filter(participante = participanteEXP).values()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    return JsonResponse({"experienciaLaboral":list(experienciasPartipante)}, status=status.HTTP_200_OK)