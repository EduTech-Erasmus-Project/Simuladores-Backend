from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView
# Create your views here.
from SimuladoresLaboralesApi.serializers import UsuarioSerializer, EvaluadorSerializer
from usuario.models import Usuario, Evaluador


class EvaluadorRetrieveAPIView(RetrieveAPIView):
        queryset = Evaluador.objects.all()
        serializer_class = EvaluadorSerializer
