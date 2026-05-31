from django.db import models
from proyectos.models.evento import Evento


class Tarea(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ]

    nombre_tarea = models.CharField(max_length=200, verbose_name='nombre de la tarea')
    descripcion = models.TextField(blank=True, verbose_name='descripción')
    fecha_limite = models.DateField(verbose_name='fecha límite')
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='media',
        verbose_name='prioridad',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='estado',
    )
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='tareas',
        verbose_name='evento',
    )

    class Meta:
        ordering = ['fecha_limite', 'prioridad']
        verbose_name = 'tarea'
        verbose_name_plural = 'tareas'

    def __str__(self):
        return f"{self.nombre_tarea} [{self.get_prioridad_display()}]"
