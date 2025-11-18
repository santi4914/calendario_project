# notas/admin.py
from django.contrib import admin
from .models import Nota # Importa nuestro modelo Nota

# Opcional: Personaliza la visualización del modelo en el admin
class NotaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'fecha_creacion', 'contenido')
    list_filter = ('fecha',)
    search_fields = ('titulo', 'contenido')
    date_hierarchy = 'fecha' # Agrega un navegador de fechas

admin.site.register(Nota, NotaAdmin) # Registra el modelo Nota con su personalización