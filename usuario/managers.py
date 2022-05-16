from django.db import models
from django.contrib.auth.models import BaseUserManager



class UsuarioManager(BaseUserManager, models.Manager):
    def _create_user(self, email, nombre, apellido, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        # if is_staff and is_superuser:
        # user.tipoUser = "admin"

        user.set_password(password)
        # user.save(using=self.db)
        return user

    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        user = self._create_user(email, nombre, apellido, password, False, False, **extra_fields)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):
        user = self._create_user(email, nombre, apellido, password, True, True, **extra_fields)
        user.tipoUser = "admin"
        user.save(using=self.db)
        return user

    def create_expert(self, email, nombre, apellido, password=None, **extra_fields):
        user = self._create_user(email, nombre, apellido, password, False, False, **extra_fields)
        user.tipoUser = "evaluador"
        user.save(using=self.db)
        return user
