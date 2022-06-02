from dataclasses import field
from msilib.schema import Class
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from SimuladoresLaboralesApi.serializers import UsuarioSerializer
from SimuladoresLaboralesApi.serializers import CompetenciaTotal
from SimuladoresLaboralesApi.serializers import Ejercitario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from usuario.models import Usuario, Participante, Evaluador



class EvaluadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = Evaluador
        fields = '__all__'

