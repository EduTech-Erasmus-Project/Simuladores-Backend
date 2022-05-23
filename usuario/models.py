import shortuuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UsuarioManager


class Evaluador(models.Model):
    APROBACION_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('rechazado', 'Rechazado'),
        ('aprobado', 'Aprobado'),
    )
    aprobacion = models.CharField(max_length=13, choices=APROBACION_CHOICES, default='pendiente')
    razon = models.TextField(default="La cuenta aún está en revisión, espere la aprobación del administrador.",
                             blank=True, null=True)
    usuario = models.OneToOneField("Usuario", on_delete=models.CASCADE, related_name='usuario_evaluador', blank=True,
                                   null=True)

    def __str__(self):
        return self.usuario.email


class Participante(models.Model):
    APROBACION_CHOICES = (
        ('sin_asignar', 'Sin Asignar'),
        ('pendiente', 'Pendiente'),
        ('rechazado', 'Rechazado'),
        ('aprobado', 'Aprobado'),
    )

    ref = models.CharField(max_length=64, default=str(shortuuid.ShortUUID().random(length=64)))
    aceptacionResponsable = models.CharField(max_length=13, choices=APROBACION_CHOICES, default='sin_asignar')
    razon = models.TextField(default="No ha elegido ningún responsable evaluador.", blank=True, null=True)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name="evaluador_participante")
    usuario = models.OneToOneField("Usuario", on_delete=models.CASCADE, related_name='usuario_participante',
                                   blank=True,
                                   null=True)

    def __str__(self):
        return self.usuario.email


# Create your models here.
class Usuario(AbstractBaseUser, PermissionsMixin):
    GENERO_CHOICES = (
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('LGBT', 'LGBT'),
    )
    ROL_CHOICES = (
        ('participante', 'Participante'),
        ('evaluador', 'Evaluador'),
        ('admin', 'Administrador'),
    )
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    pais = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True)
    fechaNacimiento = models.DateField(verbose_name='Fecha de nacimiento', blank=True, null=True)
    genero = models.CharField(max_length=7, choices=GENERO_CHOICES, blank=True, null=True)
    img = models.ImageField(upload_to='users/', max_length=250, blank=True, null=True)
    tipoUser = models.CharField(max_length=13, choices=ROL_CHOICES, default='participante')
    codigo = models.CharField(max_length=6, default=str(shortuuid.ShortUUID().random(length=6)))

    carreraUniversitaria = models.CharField(max_length=100, blank=True, null=True)
    numeroDeHijos = models.PositiveIntegerField(default=0, blank=True, null=True)
    estadoCivil = models.CharField(max_length=30, blank=True, null=True)
    etnia = models.CharField(max_length=30, blank=True, null=True)
    estudiosPrevios = models.CharField(max_length=100, blank=True, null=True)
    nivelDeFormacion = models.CharField(max_length=50, blank=True, null=True)

    is_staff = models.BooleanField(verbose_name="Django Admin", default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["nombre", "apellido"]

    def __str__(self):
        return f'Email: {self.email}, Nombre: {self.nombre}, Apellido: {self.apellido}'

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
