from django.db import models
from .evento import Evento


class Tarea(models.Model):

    class Prioridad(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"
        URGENTE = "urgente", "Urgente"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROGRESO = "en_progreso", "En Progreso"
        COMPLETADA = "completada", "Completada"
        CANCELADA = "cancelada", "Cancelada"

    nombre_tarea = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    prioridad = models.CharField(
        max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA
    )
    estado = models.CharField(
        max_length=15, choices=Estado.choices, default=Estado.PENDIENTE
    )
    evento = models.ForeignKey(
        Evento, on_delete=models.CASCADE, related_name="tareas"
    )

    class Meta:
        db_table = "tareas"
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["fecha_limite", "prioridad"]

    def __str__(self):
        return f"{self.nombre_tarea} [{self.prioridad}] - {self.estado}"
