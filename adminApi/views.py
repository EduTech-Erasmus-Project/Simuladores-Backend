
from rest_framework.response import  Response
from rest_framework.views import APIView
from SimuladoresLaboralesApi.models import Ejercitario
from SimuladoresLaboralesApi.serializers import UsuarioSerializer
from adminApi.serializers import EvaluadorSerializer

from usuario.models import Evaluador, Usuario
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

#evaluadores Pendientes
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listarEvaluadoresPendientes (request):
    if request.method == 'GET':
        evaluador = Evaluador.objects.all().filter(aprobacion='pendiente')
        evaludar_serializer = EvaluadorSerializer(evaluador,many =True)
        return Response(evaludar_serializer.data) 

#evaluador Rechazado 
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listarEvaluladoresRechazado (request):
    if request.method == 'GET':
        evaluador = Evaluador.objects.all().filter(aprobacion='rechazado')
        evaludar_serializer = EvaluadorSerializer(evaluador,many =True)
        return Response(evaludar_serializer.data) 


#Evaluador Aprobado
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listarEvaluladoresAprobados (request):
    if request.method == 'GET':
        evaluador = Evaluador.objects.all().filter(aprobacion='aprobado')
        evaludar_serializer = EvaluadorSerializer(evaluador,many =True)
        return Response(evaludar_serializer.data) 


