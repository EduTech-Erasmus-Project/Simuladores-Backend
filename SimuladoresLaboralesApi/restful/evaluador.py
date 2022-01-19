from ..models import * 
from ..serializers import * 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
#@permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getEvaluador(request,pk):
    try:
        evaluador = Evaluador.objects.get(id= pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    evaluador_serializer = EvaluadorSerializerObjectsNOPassword(evaluador)
    return Response(evaluador_serializer.data)