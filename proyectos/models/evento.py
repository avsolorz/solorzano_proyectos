from django.db import models
from proyectos.models.cliente import Cliente
from proyectos.models.usuario import Usuario


class Evento(models.Model):
    ESTADO_CHOICES = [
        ('planificacion', 'Planificación'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    nombre_evento = models.CharField(max_length=200, verbose_name='nombre del evento')
    descripcion = models.TextField(blank=True, verbose_name='descripción')
    fecha_evento = models.DateField(verbose_name='fecha del evento')
    ubicacion = models.CharField(max_length=255, blank=True, verbose_name='ubicación')
    presupuesto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='presupuesto',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='planificacion',
        verbose_name='estado',
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='eventos',
        verbose_name='cliente',
    )
    coordinador = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='eventos',
        verbose_name='coordinador',
    )

    class Meta:
        ordering = ['-fecha_evento']
        verbose_name = 'evento'
        verbose_name_plural = 'eventos'

    def __str__(self):
        return f"{self.nombre_evento} - {self.get_estado_display()}"
