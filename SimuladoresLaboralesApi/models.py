from django.db import models

# Create your models here.

#modelo para la tabla de perfil clase padre
class Perfil(models.Model):
    id = models.AutoField(primary_key=True, null= False)
    email = models.EmailField(blank=False, null= False, unique=True)
    password = models.CharField(max_length= 800, blank= False, null= False)
    nombre = models.CharField(max_length=30, blank= False, null= False)
    apellido = models.CharField(max_length=30, blank= False, null= False)
    telefono = models.CharField(max_length=10, blank= False, null= False)
    pais = models.CharField(max_length=30, blank= False, null= False)
    ciudad = models.CharField(max_length=30, blank= False, null= False)
    direccion = models.CharField(max_length=100, blank= False, null= False)
    class Meta:
        abstract = True


# modelo para la tabla de evaluador clase hija de perfil  
class Evaluador(Perfil):
    nivelDeFormacion = models.CharField(max_length=50, blank= True, null= True)

# modelo para la tabla de evaluador clase hija de perfil  
class Participante(Perfil):
    fechaNacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    carreraUniversitaria = models.CharField(max_length=100, blank= True, null= True)
    genero = models.CharField(max_length=15, blank= True, null= True)
    numeroDeHijos = models.PositiveIntegerField(default=0, blank= True, null= True)
    estadoCivil = models.CharField(max_length=30, blank= True, null= True)
    etnia = models.CharField(max_length=30, blank= True, null= True)
    estudiosPrevios = models.CharField(max_length=100, blank= True, null= True)
    codigoEstudiante = models.CharField(max_length=30, blank= True, null= True)
    nivelDeFormacion = models.CharField(max_length=50, blank= True, null= True)
    responsable = models.ForeignKey('Evaluador', on_delete=models.CASCADE, null=True, blank=True)

class DiscapacidadParticipante(models.Model):
    idGradoDeDiscapacidad = models.AutoField(primary_key=True, null= False)
    gradoDeDiscapacidad = models.PositiveIntegerField(default=0, null= True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True, related_name='DiscapacidadParticipante')
    discapacidad = models.ForeignKey('Discapacidad', on_delete=models.CASCADE, null=True, blank=True, related_name='TipoDiscapacidad')

#modelo para la tabla de experiencia laboral de un participante 
class Discapacidad(models.Model):
    idDiscapacidad = models.AutoField(primary_key=True, null= False)
    tipoDiscapacidad = models.CharField(max_length=50, blank= True, null= True, unique=True)
    
#modelo para la tabla de experiencia laboral de un participante 
class ExperienciaLaboral(models.Model):
    idExperienciaLaboral = models.AutoField(primary_key=True, null= False)
    areaLaboral = models.CharField(max_length=50, blank= True, null= True)
    aniosDeExperiencia = models.PositiveIntegerField(default=0, blank= True, null= True)
    sectorEconomico = models.CharField(max_length=50, blank= True, null= True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True, related_name='ExperienciaParticipante')

#modelo para la tabla de asiganacion actividades a un participante 
class Asignacion(models.Model):
    idAsignacion = models.AutoField(primary_key=True, null= False)
    fechaAsignacion = models.DateTimeField(auto_now=False, null= True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True,related_name='AsignacionParticipante')
    evaluador = models.ForeignKey('Evaluador', on_delete=models.CASCADE, null=True, blank=True,related_name='AsignacionEvaluador')
    ejercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True,related_name='AsignacionEjercitario')


class Ejercitario(models.Model):
    idEjercitario = models.AutoField(primary_key=True, null= False)
    numeroDeEjercitario = models.PositiveIntegerField(default=0, blank= False, null= False)
    tipoDeEjercitario = models.CharField(max_length=30, blank= False, null= False)
    nombreDeEjercitario = models.CharField(max_length=30, blank= False, null= False)
    instruccionPrincipalEjercitario = models.CharField(max_length=300, blank= False, null= False)
    principalCompetenciasEjercitario = models.CharField(max_length=100, blank= False, null= False)
    duracionEjercitarioPorMinutos =  models.PositiveIntegerField(default=0, blank= True, null= True)
    instruccionesParticipantes = models.CharField(max_length=1000, blank= False, null= False)
    urlEjercitarios = models.URLField(max_length = 200, blank= False, null= False) 

class Pregunta(models.Model):
    idPregunta = models.AutoField(primary_key=True, null= False)
    contenido = models.CharField(max_length=300, blank= False, null= False)
    respuestaCorrecta =  models.CharField(max_length=100, blank= False, null= False)
    numeroPregunta =  models.PositiveIntegerField(default=0, blank= False, null= False)
    preguntaDelEjercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True,related_name='PreguntaDeEjercitario')

#Convertir esta informacion para formatear 
class Actividad(models.Model): 
    idActividad = models.AutoField(primary_key=True, null= False)
    comentario = models.CharField(max_length=1000, blank= True, null= True)
    tiempoInicio = models.CharField(max_length=30, blank= False, null= False)
    tiempoFin =  models.CharField(max_length=30, blank= False, null= False)
    fechaDeActividad = models.DateTimeField(auto_now=False, null= True)
    ActividadPorEjercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadEjercitarioID')
    ActividadDeParticipante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadDelParticipante')
    

class Respuesta(models.Model):
    idPregunta = models.AutoField(primary_key=True, null= False)
    numeroPregunta = models.PositiveIntegerField(default=0, blank= False, null= False)
    respuestaIngresada = models.CharField(max_length=100, blank= False, null= False)
    tiempoRespuesta = models.CharField(max_length=100, blank= False, null= False)
    preguntaDeLaActividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True, blank=True,related_name='PreguntaDeActividad')
