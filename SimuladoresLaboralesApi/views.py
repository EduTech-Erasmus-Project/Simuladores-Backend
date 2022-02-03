from django.shortcuts import render
from .models import * 
from .serializers import * 
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import json

# Create your views here.
class ParticipanteViewSet(viewsets.ModelViewSet):
  queryset = Participante.objects.all()
  serializer_class = ParticipanteSerializer
  
class EvaluadorViewSet(viewsets.ModelViewSet):
  queryset = Evaluador.objects.all()
  serializer_class = EvaluadorSerializer

class ExperienciaLaboralViewSet(viewsets.ModelViewSet):
  queryset = ExperienciaLaboral.objects.all()
  serializer_class = ExperienciaLaboralSerializer

class SesionViewSet(viewsets.ModelViewSet):
  queryset = Asignacion.objects.all()
  serializer_class = SesionSerializer

class EjercitarioViewSet(viewsets.ModelViewSet):
  queryset = Ejercitario.objects.all()
  serializer_class = EjercitarioSerializer

class ActividadViewSet(viewsets.ModelViewSet):
  queryset = Actividad.objects.all()
  serializer_class = ActividadSerializer

class PreguntaViewSet(viewsets.ModelViewSet):
  queryset = Pregunta.objects.all()
  serializer_class = PreguntaSerializer

class DiscapaciadViewSet(viewsets.ModelViewSet):
  queryset = Discapacidad.objects.all()
  serializer_class = PreguntaSerializer

class GradoDiscapaciadViewSet(viewsets.ModelViewSet):
  queryset = DiscapacidadParticipante.objects.all()
  serializer_class = PreguntaSerializer
  
class ComentarioViewSet(viewsets.ModelViewSet):
  queryset = Comentario.objects.all()
  serializer_class = ComentarioSerializerObjectsModel
  
#Views to post and get for Unity

#class 

class saveUnityEjercictario(APIView):
  def post(self, request): 
    valor = request.data.get('')
    valor = request.data.get('')
    valor = request.data.get('')
    valor = request.data.get('')
  
