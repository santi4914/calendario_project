# notas/models.py
from django.db import models
from django.utils import timezone # Importa timezone para campos de fecha y hora

class Nota(models.Model):
    """
    Representa una nota asociada a una fecha específica en el calendario.

    Campos:
    - titulo: El título breve de la nota.
    - contenido: El contenido detallado de la nota (opcional).
    - fecha: La fecha a la que está asociada esta nota.
    - fecha_creacion: Marca de tiempo de cuándo se creó la nota automáticamente.
    """
    titulo = models.CharField(max_length=100, verbose_name="Título")
    contenido = models.TextField(verbose_name="Contenido", blank=True, null=True) # `blank=True` permite que sea vacío en formularios, `null=True` permite que sea nulo en DB
    fecha = models.DateField(verbose_name="Fecha")
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    def __str__(self):
        """
        Devuelve la representación en cadena del modelo, usando el título de la nota.
        """
        return self.titulo

    class Meta:
        """
        Metaclase para opciones adicionales del modelo.
        """
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ["fecha", "titulo"] # Ordenar por fecha y luego por título por defecto