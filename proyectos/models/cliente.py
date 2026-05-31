from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='nombre')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='teléfono')
    correo = models.EmailField(unique=True, verbose_name='correo electrónico')
    direccion = models.TextField(blank=True, verbose_name='dirección')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nombre
