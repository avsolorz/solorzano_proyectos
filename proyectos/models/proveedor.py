from django.db import models


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=200)
    contacto = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    servicio = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "proveedores"
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre_empresa"]

    def __str__(self):
        return f"{self.nombre_empresa} - {self.servicio}"
