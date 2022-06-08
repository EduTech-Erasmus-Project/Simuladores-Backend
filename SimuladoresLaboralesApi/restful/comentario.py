from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def getComentariosActividadRealizada(request, actividad):
    try:
        actividadCom = Actividad.objects.get(idActividad=actividad)
        comentarios = Comentario.objects.all().filter(comentarioActividad=actividadCom).order_by(
            '-fechaComentario').values()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"comentarios": list(comentarios)}, status=status.HTTP_200_OK)

'''
'''
# verificar metodo
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def agregarNuevoComentarioActividadParticipante(request):
    try:
        comentarioNew = {
            'comentario': request.data.get("comentario"),
            'fechaComentario': request.data.get("fecha"),
            'comentarioActividad': request.data.get("actividad")
        }
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    comentario_serializer = ComentarioSerializerObjectsModel(data=comentarioNew)

    if comentario_serializer.is_valid():
        comentario_serializer.save()
        return Response(comentario_serializer.data, status=status.HTTP_201_CREATED)

    return Response(comentario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''