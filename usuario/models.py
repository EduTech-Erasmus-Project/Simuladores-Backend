from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class PerfilManager(BaseUserManager):

    def create_user(self, nombre, apellido, password, email):
        usuario = self.model(
            nombre=nombre,
            apellido=apellido,
            email=self.normalize_email(email),
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, nombre, apellido, password, email):
        usuario = self.create_user(
            nombre=nombre,
            apellido=apellido,
            password=password,
            email=email,
        )
        usuario.tipoUser = "admin"
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser):
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
    email = models.EmailField(blank=False, null=False, unique=True)
    nombre = models.CharField(max_length=30, blank=False, null=False)
    apellido = models.CharField(max_length=30, blank=False, null=False)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True, blank=True, null=True)
    fechaNacimiento = models.DateField(verbose_name='Fecha de nacimiento', blank=True, null=True)
    genero = models.CharField(max_length=7, choices=GENERO_CHOICES, blank=True, null=True)
    img = models.ImageField(upload_to='perfil/', max_length=250, blank=True, null=True)
    tipoUser = models.CharField(max_length=13, choices=ROL_CHOICES, blank=True, null=True, default='Participante')
    object = PerfilManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["nombre", "apellido"]

    def __str__(self):
        return f'Email: {self.email}'

    def has_perm(self, perm, ob=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.tipoUser == "admin"

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
