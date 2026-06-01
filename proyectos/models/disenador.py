from django.db import models


class Disenador(models.Model):
    nombre = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(unique=True)

    class Meta:
        db_table = "disenadores"
        verbose_name = "Diseñador"
        verbose_name_plural = "Diseñadores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
