from os import sep, stat
from urllib.request import Request
from rest_framework.response import  Response
from rest_framework.views import APIView
from SimuladoresLaboralesApi.serializers import UsuarioListaSerializer, UsuarioSerializer
from adminApi.serializers import EvaluadorSerializer
from usuario.models import Evaluador, Usuario
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from SimuladoresLaboralesApi.models import DiscapacidadParticipante
from SimuladoresLaboralesApi.serializers import UsuarioSerializer, EvaluadorSerializer, PerfilSerializers, \
    ActualizarPerfilSerializers
from usuario.models import Usuario, Evaluador, Participante


class EvaluadorRetrieveAPIView(RetrieveAPIView):
    queryset = Evaluador.objects.all()
    serializer_class = EvaluadorSerializer


class MiPefilAPIView(APIView):

    def get(self, request):
        user = Usuario.objects.get(id=self.request.user.id)
        serializer = PerfilSerializers(user)
        data = serializer.data
        try:
            discapacidades = DiscapacidadParticipante.objects.filter(participante__usuario_id=data["id"]).values()
            data["discapacidades"] = discapacidades
        except:
            pass

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        discapacidades = request.data["discapacidades"]

        serializer = ActualizarPerfilSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            userUpdate = Usuario.objects.get(id=user.id)
            for key, value in data.items():
                setattr(userUpdate, key, value)
            userUpdate.save()

            if user.tipoUser == "participante" and len(discapacidades) > 0:
                for discapacidad in discapacidades:
                    participante = Participante.objects.get(usuario_id=user.id)
                    updated_values = {'gradoDeDiscapacidad': discapacidad["grado"], "discapacidad_id": discapacidad["id"], "participante_id": participante.id}
                    try:
                        obj = DiscapacidadParticipante.objects.get(gradoDeDiscapacidad=discapacidad["grado"], participante_id=participante.id, discapacidad_id=discapacidad["id"])
                        for key, value in updated_values.items():
                            setattr(obj, key, value)
                        obj.save()
                    except DiscapacidadParticipante.DoesNotExist:
                        obj = DiscapacidadParticipante(gradoDeDiscapacidad=discapacidad["grado"], participante_id=participante.id, discapacidad_id=discapacidad["id"])
                        obj.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def actualizarPassword(request):
    user = request.user
    oldPass = request.data.get('oldPassword')
    newPass = request.data.get('newPassword')
    if user.check_password(oldPass):
        user.set_password(newPass)
        user.save()
        return Response({"status": "ok", "code": "ok"}, status=status.HTTP_200_OK)
    else:
        return Response({"estaus": "error", "code": "old_password_no_valid"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def listarUsuarioRegistrado (request):
    if request.method == 'GET':
        usuario = Usuario.objects.all().filter(tipoUser='participante')
        usuario_serializer =UsuarioSerializer(usuario,many =True)
        return Response(usuario_serializer.data) 


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bloqueoUsuario(request,pk=None):
    if request.method == 'GET':
        usuario = Usuario.objects.get(id=pk)
        if usuario.estado == True:
            usuario.estado=False
            usuario.save()
            usuario_serilizer = UsuarioSerializer(usuario)
            return Response(usuario_serilizer.data, status=status.HTTP_200_OK)
        elif usuario.estado == False:
            usuario.estado=True
            usuario.save()
            usuario_serilizer = UsuarioSerializer(usuario)
            return Response(usuario_serilizer.data, status=status.HTTP_200_OK)

# def create_learning_object(request, user_token, Serializer, areas, method):
#     uuid = str(shortuuid.shortUUID().random(length=8))
#     file = request.FILES['file']

#     file._name = file._name.split('.')[0] + "_" + uuid + "." + file._name.split('.')[1]

#     path="uploads"
#     file_name = file._name
#     directory_origin

# @api_view(['POST'])
# def api_upload(request):
#     if "file" not in request.FILES:
#         return Response(
#             {"status": False, "message": "The zip is required in the request.", "code":"required_file"},
#             status=status.HTTP_400_BAD_REQUEST) 

#     if request.FILES["file"].name.split(sep='.')[-1] != "zip":
#         return Response(
#             {"status": False, "message": "The file is not a .zip, a file with a .zip extension is required.", 
#             "code":"incorrect_format"},
#             status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         api_data = RequestApi.objects.get(api_key=request.GET.get('api_key', None))
#         areas = request.GET.get('adaptation', None).split(sep=',')
#         serializer, learning_object, is_adapted = create_learning_objects(request, api_data.api_key,ApiLearningObjectDetailSerializer,areas,"automatic")

#         if is_adapted:
#             return Response(
#                 {"state": "learning_Object_Adapted"}, status=status.HTTP_400_BAD_REQUEST)

#         state = automatic_adaptation(areas, request, learning_object)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         print("error", e)
#     return Response(
#         {
#             "status": False, "message": "The acces key to the api is not valid", 
#             "code":"invalid_api_key"
#         },
#         status=status.HTTP_401_UNAUTHORIZED)