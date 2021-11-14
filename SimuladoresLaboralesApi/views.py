from django.shortcuts import render
from .models import * 
from .serializers import * 
from rest_framework import viewsets

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
  queryset = Sesion.objects.all()
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