from django.db import models

# Create your models here.

class Perfil(models.Model):
    id = models.AutoField(primary_key=True, null= False)
    email = models.EmailField(blank=False, null= False)
    password = models.CharField(max_length= 20, blank= False, null= False)
    nombre = models.CharField(max_length=30, blank= False, null= False)
    apellido = models.CharField(max_length=30, blank= False, null= False)
    telefono = models.CharField(max_length=10, blank= False, null= False)
    pais = models.CharField(max_length=30, blank= False, null= False)
    ciudad = models.CharField(max_length=30, blank= False, null= False)
    direccion = models.CharField(max_length=100, blank= False, null= False)
    class Meta:
        abstract = True

class ExperienciaLaboral(models.Model):
    idExperienciaLaboral = models.AutoField(primary_key=True, null= False)
    areaLaboral = models.CharField(max_length=50, blank= True, null= True)
    aniosDeExperiencia = models.PositiveIntegerField(default=0, blank= True, null= True)
    sectorEconomico = models.CharField(max_length=50, blank= True, null= True)
    participante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True)
    
class Evaluador(Perfil):
    nivelDeFormacion = models.CharField(max_length=50, blank= True, null= True)


class Participante(Perfil):
    gradoDeDiscapacidad = models.PositiveIntegerField(default=0, null= True)
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


class Sesion(models.Model):
    idSesion = models.AutoField(primary_key=True, null= False)
    fechaSesion = models.DateTimeField(auto_now=True, null= False)
    sesionDelParticipante = models.ForeignKey('Participante', on_delete=models.CASCADE, null=True, blank=True)

class Ejercitario(models.Model):
    idActividad = models.AutoField(primary_key=True, null= False)
    numeroDeEjercitario = models.PositiveIntegerField(default=0, blank= True, null= True)
    tipoDeEjercitario = models.CharField(max_length=30, blank= False, null= False)
    nombreDeEjercitario = models.CharField(max_length=30, blank= False, null= False)
    instruccionPrincipalEjercitario = models.CharField(max_length=300, blank= False, null= False)
    principalCompetenciasEjercitario = models.CharField(max_length=100, blank= False, null= False)
    duracionEjercitarioPorMinutos =  models.PositiveIntegerField(default=0, blank= True, null= True)
    instruccionesParticipantes = models.CharField(max_length=300, blank= False, null= False)
    urlEjercitarios = models.URLField(max_length = 200, blank= False, null= False) 

#Convertir esta informacion para formatear 
class Actividad(models.Model): 
    idActividad = models.AutoField(primary_key=True, null= False)
    comentario = models.CharField(max_length=1000, blank= True, null= True)
    tiempoInicio = models.CharField(max_length=30, blank= False, null= False)
    tiempoFin =  models.CharField(max_length=30, blank= False, null= False)
    sesionPorActividad = models.ForeignKey('Sesion', on_delete=models.CASCADE, null=True, blank=True)
    ActividadPorEjercitario = models.ForeignKey('Ejercitario', on_delete=models.CASCADE, null=True, blank=True)

class Pregunta(models.Model):
    idActividad = models.AutoField(primary_key=True, null= False)
    contenido = models.CharField(max_length=300, blank= False, null= False)
    respuesta = models.CharField(max_length=100, blank= False, null= False)
    respuestaObtenida = models.CharField(max_length=100, blank= False, null= False)
    tiempoRespuesta = models.CharField(max_length=100, blank= False, null= False)
    preguntaDeLaActividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True, blank=True)
