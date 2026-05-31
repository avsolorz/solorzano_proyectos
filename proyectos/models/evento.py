from django.db import models
from django.conf import settings
from .cliente import Cliente


class Evento(models.Model):

    class Estado(models.TextChoices):
        PLANIFICADO = "planificado", "Planificado"
        EN_PROGRESO = "en_progreso", "En Progreso"
        COMPLETADO = "completado", "Completado"
        CANCELADO = "cancelado", "Cancelado"

    nombre_evento = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_evento = models.DateField()
    ubicacion = models.CharField(max_length=255, blank=True)
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PLANIFICADO
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="eventos"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="eventos"
    )

    class Meta:
        db_table = "eventos"
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["fecha_evento"]

    def __str__(self):
        return f"{self.nombre_evento} | {self.fecha_evento} | {self.estado}"
