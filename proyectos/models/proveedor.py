from django.db import models


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=200, verbose_name='nombre de empresa')
    contacto = models.CharField(max_length=150, blank=True, verbose_name='contacto')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='teléfono')
    correo = models.EmailField(unique=True, verbose_name='correo electrónico')
    servicio = models.CharField(max_length=200, blank=True, verbose_name='servicio')

    class Meta:
        ordering = ['nombre_empresa']
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'

    def __str__(self):
        return f"{self.nombre_empresa} - {self.servicio}"
