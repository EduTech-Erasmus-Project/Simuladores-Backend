from django.db import models
# Create your models here.



class Administrador():
    ROL_CHOICES = (
        ('participante', 'Participante'),
        ('evaluador', 'Evaluador'),
        ('admin', 'Administrador'),
    )
    #tipoUser = models.CharField(max_length=13, choices=ROL_CHOICES, blank=False, null=False, default='admin')