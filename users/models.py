from django.db import models

# Create your models here.
class Perfil(models.Model):
    id=models.CharField(max_length=5, primary_key=True)
    nick=models.CharField(max_length=15)
    clave=models.CharField(max_length=12)
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    telefono=models.CharField(max_length=10)