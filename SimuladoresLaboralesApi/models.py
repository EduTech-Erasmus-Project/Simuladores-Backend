import shortuuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from usuario.models import Participante, Evaluador


class Discapacidad(models.Model):
    tipoDiscapacidad = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.tipoDiscapacidad


class DiscapacidadParticipante(models.Model):
    gradoDeDiscapacidad = models.PositiveIntegerField(default=0, null=True)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='DiscapacidadParticipante')
    discapacidad = models.ForeignKey(Discapacidad, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='TipoDiscapacidad')

    def __str__(self):
        return self.gradoDeDiscapacidad


class ExperienciaLaboral(models.Model):
    areaLaboral = models.CharField(max_length=50, blank=True, null=True)
    aniosDeExperiencia = models.PositiveIntegerField(default=0, blank=True, null=True)
    sectorEconomico = models.CharField(max_length=50, blank=True, null=True)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='ExperienciaParticipante')

    def __str__(self):
        return self.areaLaboral


class Competencia(models.Model):
    titulo = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.titulo


class Ejercitario(models.Model):
    LEVEL_CHOICES = (
        ('Nivel1', 'Nivel 1'),
        ('Nivel2', 'NIvel 2'),
        ('Nivel3', 'NIvel 3'),
    )
    # numeroDeEjercitario = models.PositiveIntegerField(default=0, unique=True, blank=False, null=False)
    tipoDeEjercitario = models.CharField(max_length=30, blank=False, null=False)
    nombreDeEjercitario = models.CharField(max_length=256, blank=False, null=False)
    instruccionPrincipalEjercitario = models.TextField(blank=False, null=False)
    variaciones = models.TextField(blank=True, null=True)
    duracion = models.PositiveIntegerField(default=0, blank=True, null=True)
    instruccionesParticipantes = models.TextField(blank=False, null=False)
    urlEjercitario = models.URLField(max_length=200, blank=False, null=False)
    nivel = models.CharField(max_length=7, choices=LEVEL_CHOICES, blank=True, null=True)
    categoria = models.CharField(max_length=256, blank=True, null=True)
    sector = models.CharField(max_length=256, blank=True, null=True)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='competencia_ejercitario')

    def __str__(self):
        return str(self.id) + " - " + self.nombreDeEjercitario


''' 
# modelo para la tabla de asiganacion actividades a un participante
class Asignacion(models.Model):
    fechaAsignacion = models.DateTimeField(auto_now=False, null=True)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='AsignacionParticipante')
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='AsignacionEvaluador')
    #ejercitario = models.ForeignKey(Ejercitario, on_delete=models.CASCADE, null=True, blank=True,
                                    #related_name='AsignacionEjercitario')
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, null=True, blank=True, related_name='asignacion_competencia')
'''


class Pregunta(models.Model):
    contenido = models.CharField(max_length=300, blank=False, null=False)
    respuestaCorrecta = models.CharField(max_length=100, blank=False, null=False)
    numeroPregunta = models.PositiveIntegerField(default=0, blank=False, null=False)
    preguntaDelEjercitario = models.ForeignKey(Ejercitario, on_delete=models.CASCADE, null=True, blank=True,
                                               related_name='preguntaDeEjercitario')


# Convertir esta informacion para formatear
class Actividad(models.Model):
    tiempoInicio = models.CharField(max_length=30, blank=False, null=False)
    tiempoFin = models.CharField(max_length=30, blank=False, null=False)
    tiempoTotal = models.DecimalField(default=0, blank=False, null=False, max_digits=5, decimal_places=2)
    fecha = models.DateTimeField(auto_now=False, null=True)
    preguntasCorrectas = models.PositiveIntegerField(default=0, blank=False, null=False)
    preguntasContestadas = models.PositiveIntegerField(default=0, blank=False,
                                                       null=False)
    totalPreguntas = models.PositiveIntegerField(default=0, blank=False, null=False)
    calificacion = models.PositiveIntegerField(default=0, blank=False, null=False)
    #calificacionPorcentaje = models.PositiveIntegerField(default=0, blank=False, null=False)
    ejercitario = models.ForeignKey(Ejercitario, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='actividad_ejercitario')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='actividad_participante')


class Comentario(models.Model):
    comentario = models.TextField(blank=False, null=False)
    fechaComentario = models.DateTimeField(auto_now_add=True, null=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='comentario_actividad')
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='comentario_participante')
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='comentario_evaluador')


class Respuesta(models.Model):
    numeroPregunta = models.PositiveIntegerField(default=0, blank=False, null=False)
    respuestaIngresada = models.CharField(max_length=100, blank=False, null=False)
    tiempoRespuesta = models.CharField(max_length=100, blank=False, null=False)
    preguntaDeLaActividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null=True, blank=True,
                                              related_name='PreguntaDeActividad')
