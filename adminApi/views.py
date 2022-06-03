
from rest_framework.response import  Response
from rest_framework.views import APIView
from SimuladoresLaboralesApi.models import Ejercitario
from SimuladoresLaboralesApi.serializers import UsuarioSerializer
from adminApi.serializers import EvaluadorSerializer
from rest_framework import status
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



#Competencia Aprobar
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def aprobarEvaluador(request):
    idUsuario = request.data.get('idU')
    idEvaluador =request.data.get('idE')
    razon = request.data.get('razon')
    aprobacion = request.data.get('estado')

    try:
        evaluador = Evaluador.objects.get(id=idEvaluador, usuario_id=idUsuario)
    except:
        return Response({"status": "error", "code": "not_found_participante"}, status=status.HTTP_404_NOT_FOUND)

    if aprobacion:
        evaluador.aprobacion = "aprobado"
        evaluador.razon = ""
    else:
        if razon == "":
            return Response({"status": "error", "code": "not_found_razon"}, status=status.HTTP_400_BAD_REQUEST)

        evaluador.aprobacion = "rechazado"
        evaluador.razon = razon
    evaluador.save()

    return Response({"status": "ok", "code": "ok"}, status=status.HTTP_200_OK)