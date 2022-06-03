
<<<<<<< HEAD
=======
from dataclasses import field
from msilib.schema import Class
from django.contrib.auth.models import update_last_login
from SimuladoresLaboralesApi.models import Ejercitario
from SimuladoresLaboralesApi.serializers import CompetenciaTotal
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from usuario.models import Usuario
from .models import *

>>>>>>> Fabian
