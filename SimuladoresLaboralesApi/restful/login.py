from datetime import datetime
from multiprocessing import AuthenticationError

import jwt
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from unityREST import settings
from ..mixins import IsAdmin, IsExpert
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.core import serializers
import hashlib

'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def verificarExistenciaCorreo(request):
    correo = request.data.get('correo')
    tipoUserParticipante = ''
    tipoUserEvaluador = ''
    try:
        tipoUserParticipante = Participante.objects.get(email=correo)
    except Participante.DoesNotExist:
        print("Error en busqueda de correo en participantes")

    if (tipoUserParticipante != '' and (tipoUserParticipante.estado == "activo") and (
            tipoUserParticipante.aceptacionPendianteResponsable == "aceptado")):
        return Response({'tipoUsuario': 'participante'}, status=status.HTTP_200_OK)

    try:
        tipoUserEvaluador = Evaluador.objects.get(email=correo)
    except Evaluador.DoesNotExist:
        print("Error en busqueda de correo en evaluador")

    if (tipoUserEvaluador != '' and (tipoUserEvaluador.estado == "activo")):
        return Response({'tipoUsuario': 'evaluador'}, status=status.HTTP_200_OK)

    return Response({'tipoUsuario': 'notExist'}, status=status.HTTP_200_OK)
'''

''' 
def passwordEncriptacion(password):
    encoded = password.encode()
    encryptPW = hashlib.sha256(encoded)
    return encryptPW.hexdigest()
'''


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(
            username=email,
            password=password
        )
        print(user)
        if user:
            if not user.estado:
                return Response({"code": "user_inactive", "message": "Usuario inactivo"},
                                status=status.HTTP_400_BAD_REQUEST)
            if user.tipoUser == "evaluador":
                evaluador = Evaluador.objects.get(usuario_id=user.id)
                if evaluador.aprobacion == "pendiente":
                    return Response(
                        {"code": "user_unapproved", "message": "Evaluador no aprobado", "razon": evaluador.razon},
                        status=status.HTTP_400_BAD_REQUEST)

                if evaluador.aprobacion == "rechazado":
                    return Response(
                        {"code": "user_rejected", "message": "Evaluador rechazado", "razon": evaluador.razon},
                        status=status.HTTP_400_BAD_REQUEST)

            if user.tipoUser == "participante":
                participante = Participante.objects.get(usuario_id=user.id)
                if participante.aceptacionResponsable == "pendiente":
                    return Response(
                        {"code": "user_unapproved", "message": "Usuario no aprobado", "razon": participante.razon},
                        status=status.HTTP_400_BAD_REQUEST)

                if participante.aceptacionResponsable == "rechazado":
                    return Response(
                        {"code": "user_rejected", "message": "Usuario rechazado", "razon": participante.razon},
                        status=status.HTTP_400_BAD_REQUEST)

            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                usuario_Serializer = LoginUserSerializer(user).data
                if user.tipoUser == "participante":
                    participante = Participante.objects.get(usuario_id=user.id)
                    participante_serializer = ParticipanteLoginSerializer(participante)
                    usuario_Serializer["participante"] = participante_serializer.data

                return Response({
                    "token_access": login_serializer.validated_data.get("access"),
                    "token_refresh": login_serializer.validated_data.get("refresh"),
                    "user": usuario_Serializer
                }, status=status.HTTP_200_OK)
        return Response({"code": "user_invalid", "message": "Email or password invalid"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))  # IsExpert IsUser IsAdmin
def logout(request):
    print(request)
    user = get_object_or_404(Usuario, pk=request.user.id)
    if user is not None:
        RefreshToken.for_user(user)
        return Response({"code": "ok", "message": "Sesion cerrada con exito"}, status=status.HTTP_200_OK)


''' 
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    correo = request.data.get('email')
    password = request.data.get('password')
    passwd = passwordEncriptacion(password)

    user = None

    try:
        user = Participante.objects.get(email=correo)
    except Participante.DoesNotExist:
        pass

    try:
        user = Evaluador.objects.get(email=correo)
        if not user.aprobacion:
            return Response({'login': 'false', 'code': 'unapprovedAccount'}, status=status.HTTP_400_BAD_REQUEST)

    except Evaluador.DoesNotExist:
        pass

    if user is None:
        return Response({'code': 'notExist'}, status=status.HTTP_400_BAD_REQUEST)

    if user.password != passwd:
        print("passs incorrect")
        return Response({'code': 'incorrectCredentials'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # print(key)
        # refresh = RefreshToken.for_user(user)
        payload = {
            "id": user.id,
            'email': user.email,
            'tipoUser': user.tipoUser,
        }
        token = jwt.encode(payload, settings.TOKEN_KEY, algorithm='HS256')

        return Response({'login': 'true', 'user': {
            'id': user.id,
            'email': user.email,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'tipoUser': user.tipoUser,
        },
                         # 'refresh': str(refresh),
                         'access': token,
                         }, status=status.HTTP_200_OK)

    except Participante.DoesNotExist:
        return Response({'login': 'false'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response
'''

'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def refreshToken(request):
    token = request.data.get('jwt')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('Sin Autentificación!')
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    payload['iat'] = datetime.datetime.utcnow()

    return Response(payload)
'''
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def recuperarUsuarioCookiesJWT(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationError('Sin Autentificación!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('Sin Autentificación!')

    tipoUser = payload['tipoUser']
    if (tipoUser == 'evaluador'):
        evaluador = Evaluador.objects.get(email=payload['email'])
        serializerUser = EvaluadorSerializerObjectsNOPassword(evaluador)
        return Response(serializerUser.data)

    if (tipoUser == 'participante'):
        participante = Participante.objects.get(email=payload['email'])
        serializerUser = ParticipanteSerializerObjectsNOPassword(participante)
        return Response(serializerUser.data)
'''


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def changePassword(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    newPassword = request.data.get('newPassword')
    passwd = passwordEncriptacion(password)
    try:
        participante = Participante.objects.get(email=email, password=passwd)
    except:
        return Response({'change': 'notSame'}, status=status.HTTP_404_NOT_FOUND)

    newpasswd = passwordEncriptacion(newPassword)
    participante.password = newpasswd
    try:
        participante.save()
        return Response({'change': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'change': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
# @permission_classes((permissions.IsAuthenticated, permissions.BasePermission))
def changePasswordResponsable(request):
    email = request.data.get('correo')
    password = request.data.get('password')
    newPassword = request.data.get('newPassword')
    passwd = passwordEncriptacion(password)
    try:
        evaluador = Evaluador.objects.get(email=email, password=passwd)
    except:
        return Response({'change': 'notSame'}, status=status.HTTP_404_NOT_FOUND)

    newpasswd = passwordEncriptacion(newPassword)
    evaluador.password = newpasswd
    try:
        evaluador.save()
        return Response({'change': 'ok'}, status=status.HTTP_200_OK)
    except:
        return Response({'change': 'error'}, status=status.HTTP_400_BAD_REQUEST)
