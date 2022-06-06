from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
# Create your views here.
from rest_framework.views import APIView
from pathlib import Path
import os

from SimuladoresLaboralesApi.models import DiscapacidadParticipante
from SimuladoresLaboralesApi.serializers import UsuarioSerializer, EvaluadorSerializer, PerfilSerializers, \
    ActualizarPerfilSerializers
from usuario.models import Usuario, Evaluador, Participante

BASE_DIR = Path(__file__).resolve().parent.parent

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

            if user.tipoUser == "participante":
                participante = Participante.objects.get(usuario_id=user.id)
                DiscapacidadParticipante.objects.filter(participante_id=participante.id).delete()
                for discapacidad in discapacidades:

                    obj = DiscapacidadParticipante(gradoDeDiscapacidad=discapacidad["grado"],
                                                   participante_id=participante.id, discapacidad_id=discapacidad["id"])
                    obj.save()
                    '''
                    try:
                        obj = DiscapacidadParticipante.objects.get(gradoDeDiscapacidad=discapacidad["grado"], participante_id=participante.id, discapacidad_id=discapacidad["id"])
                        for key, value in updated_values.items():
                            setattr(obj, key, value)
                        obj.save()
                    except DiscapacidadParticipante.DoesNotExist:
                        obj = DiscapacidadParticipante(gradoDeDiscapacidad=discapacidad["grado"], participante_id=participante.id, discapacidad_id=discapacidad["id"])
                        obj.save()
                    '''

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


@api_view(['PUT'])
def actualizarImagenPerfil(request):
    user = request.user
    img = request.FILES["file"]

    try:
        if user.img is not None:
            user.img.delete(save=False)

        user.img = img
        user.save()
        serializer = UsuarioSerializer(user)
        return Response({"status": "ok", "code": "ok", "user": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"status": "error", "code": "error_on_upload"}, status=status.HTTP_400_BAD_REQUEST)
