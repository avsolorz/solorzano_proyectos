from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('coordinador', 'Coordinador'),
        ('asistente', 'Asistente'),
    ]

    username = None
    nombre = models.CharField(max_length=100, verbose_name='nombre')
    apellido = models.CharField(max_length=100, verbose_name='apellido')
    correo = models.EmailField(unique=True, verbose_name='correo electrónico')
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='asistente',
        verbose_name='rol',
    )

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        ordering = ['correo']
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"
