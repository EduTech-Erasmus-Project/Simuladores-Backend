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

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registrarExperienciaLaboral(request): 
    
    correo = request.data.get('correo')
    try:
        participanteSeleccionado = Participante.objects.get(email=correo)  
    except Participante.DoesNotExist: 
        return Response({'participante': 'noExist'}, status=status.HTTP_404_NOT_FOUND) 
    
    experienciaLaboralRegistrar = {
        'areaLaboral' :  request.data.get('areaLaboral'),
        'aniosDeExperiencia' : request.data.get('experienciaAnios'),
        'sectorEconomico' : request.data.get('sectorEconomico'),
        'participante' : participanteSeleccionado.id
    }
    
    experienciaLaboralRegistrar_serializer = ExperienciaLaboralSerializerObjects(data=experienciaLaboralRegistrar)
    if experienciaLaboralRegistrar_serializer.is_valid():
        experienciaLaboralRegistrar_serializer.save()
        return Response({"status": "experiencia registrada"}, status=status.HTTP_201_CREATED) 
    
    return Response(experienciaLaboralRegistrar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)