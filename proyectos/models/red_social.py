from django.db import models


class RedSocial(models.Model):
    nombre_red = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "redes_sociales"
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        ordering = ["nombre_red"]

    def __str__(self):
        return self.nombre_red
