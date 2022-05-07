from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
##modelo para autorizacion

# modelo para la tabla de perfil clase padre
class Perfil(models.Model):
    GENERO_CHOICES = (
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('LGBT', 'LGBT'),
    )
    id = models.AutoField(primary_key=True, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=800, blank=False, null=False)
    nombre = models.CharField(max_length=30, blank=False, null=False)
    apellido = models.CharField(max_length=30, blank=False, null=False)
    telefono = models.CharField(max_length=10, blank=False, null=False)
    pais = models.CharField(max_length=30, blank=False, null=False)
    ciudad = models.CharField(max_length=30, blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=False, null=False)
    estado = models.BooleanField(blank=True, null=True, default=True)
    fechaNacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=7, choices=GENERO_CHOICES, blank=True, null=True)
    img = models.ImageField(upload_to='profile', max_length=250, blank=True, null=True)


    class Meta:
        abstract = True


# modelo para la tabla de evaluador clase hija de perfil  
class Evaluador(Perfil):
    ROL_CHOICES = (
        ('participante', 'Participante'),
        ('evaluador', 'Evaluador'),
        ('admin', 'Administrador'),
    )
    aprobacion = models.BooleanField(default=False)
    tipoUser = models.CharField(max_length=13, choices=ROL_CHOICES, blank=True, null=True, default='evaluador')
    nivelDeFormacion = models.CharField(max_length=50, blank=True, null=True)


# modelo para la tabla de evaluador clase hija de perfil
class Participante(Perfil):
    ROL_CHOICES = (
        ('participante', 'Participante'),
        ('evaluador', 'Evaluador'),
        ('admin', 'Administrador'),
    )
    carreraUniversitaria = models.CharField(max_length=100, blank=True, null=True)
    numeroDeHijos = models.PositiveIntegerField(default=0, blank=True, null=True)
    estadoCivil = models.CharField(max_length=30, blank=True, null=True)
    etnia = models.CharField(max_length=30, blank=True, null=True)
    estudiosPrevios = models.CharField(max_length=100, blank=True, null=True)
    codigoEstudiante = models.CharField(max_length=30, blank=True, null=True)
    nivelDeFormacion = models.CharField(max_length=50, blank=True, null=True)
    aceptacionPendianteResponsable = models.CharField(max_length=100, blank=False, null=False, default='faltaAceptacion')
    tipoUser = models.CharField(max_length=13, choices=ROL_CHOICES, blank=True, null=True, default='participante')
    responsable = models.ForeignKey('Evaluador', on_delete=models.CASCADE, null=True, blank=True)


class DiscapacidadParticipante(models.Model):
    idGradoDeDiscapacidad = models.AutoField(primary_key=True, null=False)
    gradoDeDiscapacidad = models.PositiveIntegerField(default=0, null=True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='DiscapacidadParticipante')
    discapacidad = models.ForeignKey('Discapacidad', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='TipoDiscapacidad')


# modelo para la tabla de experiencia laboral de un participante
class Discapacidad(models.Model):
    idDiscapacidad = models.AutoField(primary_key=True, null=False)
    tipoDiscapacidad = models.CharField(max_length=50, blank=True, null=True, unique=True)


# modelo para la tabla de experiencia laboral de un participante
class ExperienciaLaboral(models.Model):
    idExperienciaLaboral = models.AutoField(primary_key=True, null=False)
    areaLaboral = models.CharField(max_length=50, blank=True, null=True)
    aniosDeExperiencia = models.PositiveIntegerField(default=0, blank=True, null=True)
    sectorEconomico = models.CharField(max_length=50, blank=True, null=True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='ExperienciaParticipante')


# modelo para la tabla de asiganacion actividades a un participante
class Asignacion(models.Model):
    idAsignacion = models.AutoField(primary_key=True, null=False)
    fechaAsignacion = models.DateTimeField(auto_now=False, null=True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='AsignacionParticipante')
    evaluador = models.ForeignKey('Evaluador', on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='AsignacionEvaluador')
    ejercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='AsignacionEjercitario')


class Competencia(models.Model):
    idCompetencia = models.AutoField(primary_key=True, null=False)
    titulo = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)

class Ejercitario(models.Model):
    LEVEL_CHOICES = (
        ('Nivel1', 'Nivel 1'),
        ('NIvel2', 'NIvel 2'),
        ('NIvel3', 'NIvel 3'),
    )
    idEjercitario = models.AutoField(primary_key=True, null=False)
    numeroDeEjercitario = models.PositiveIntegerField(default=0, unique=True, blank=False, null=False)
    tipoDeEjercitario = models.CharField(max_length=30, blank=False, null=False)
    nombreDeEjercitario = models.CharField(max_length=256, blank=False, null=False)
    instruccionPrincipalEjercitario = models.TextField(blank=False, null=False)
    principalCompetenciasEjercitario = models.CharField(max_length=50, blank=True, null=True)
    duracionEjercitarioPorMinutos = models.PositiveIntegerField(default=0, blank=True, null=True)
    instruccionesParticipantes = models.TextField(blank=False, null=False)
    urlEjercitarios = models.URLField(max_length=200, blank=False, null=False)
    nivel = models.CharField(max_length=7, choices=LEVEL_CHOICES, blank=True, null=True)
    competencia = models.ForeignKey('Competencia', on_delete=models.CASCADE, null=True, blank=True,
                                               related_name='Competencia')


class Pregunta(models.Model):
    idPregunta = models.AutoField(primary_key=True, null=False)
    contenido = models.CharField(max_length=300, blank=False, null=False)
    respuestaCorrecta = models.CharField(max_length=100, blank=False, null=False)
    numeroPregunta = models.PositiveIntegerField(default=0, blank=False, null=False)
    preguntaDelEjercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True,
                                               related_name='PreguntaDeEjercitario')


class Comentario(models.Model):
    idComentario = models.AutoField(primary_key=True, null=False)
    comentario = models.TextField(blank=False, null=False)
    fechaComentario = models.DateTimeField(auto_now=False, null=True)
    comentarioActividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True, blank=True,
                                            related_name='ComentarioDeActividad')


# Convertir esta informacion para formatear
class Actividad(models.Model):
    idActividad = models.AutoField(primary_key=True, null=False)
    comentario = models.CharField(max_length=1000, blank=True, null=True)
    tiempoInicio = models.CharField(max_length=30, blank=False, null=False)
    tiempoFin = models.CharField(max_length=30, blank=False, null=False)
    tiempoTotalResolucionEjercitario = models.PositiveIntegerField(default=0, blank=False, null=False)
    fechaDeActividad = models.DateTimeField(auto_now=False, null=True)
    totalRespuestasCorrectasIngresadasParticipante = models.PositiveIntegerField(default=0, blank=False, null=False)
    numeroTotalDeRespuestasContestadasPorElParticipante = models.PositiveIntegerField(default=0, blank=False,
                                                                                      null=False)
    numeroTotalDePreguntasDelEjercitario = models.PositiveIntegerField(default=0, blank=False, null=False)
    calificacionActividad = models.PositiveIntegerField(default=0, blank=False, null=False)
    ActividadPorEjercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True,
                                                related_name='ActividadEjercitarioID')
    ActividadDeParticipante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True,
                                                related_name='ActividadDelParticipante')


class Respuesta(models.Model):
    idPregunta = models.AutoField(primary_key=True, null=False)
    numeroPregunta = models.PositiveIntegerField(default=0, blank=False, null=False)
    respuestaIngresada = models.CharField(max_length=100, blank=False, null=False)
    tiempoRespuesta = models.CharField(max_length=100, blank=False, null=False)
    preguntaDeLaActividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True, blank=True,
                                              related_name='PreguntaDeActividad')
