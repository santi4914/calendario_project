# notas/urls.py
from django.urls import path
from . import views  # Importa las vistas de nuestra app

app_name = (
    "notas"  # Namespace de la aplicación para evitar conflictos de nombres de URLs
)

urlpatterns = [
    path(
        "", views.CalendarioView.as_view(), name="calendario"
    ),  # Vista principal del calendario
    path(
        "<int:year>/<int:month>/", views.CalendarioView.as_view(), name="calendario_mes"
    ),  # Navegación por mes/año
    path(
        "crear/<int:year>/<int:month>/<int:day>/",
        views.NotaCreateView.as_view(),
        name="crear_nota",
    ),  # Crear nota para un día
    path(
        "detalle/<int:pk>/", views.NotaDetailView.as_view(), name="detalle_nota"
    ),  # Ver detalle de una nota
    path(
        "editar/<int:pk>/", views.NotaUpdateView.as_view(), name="editar_nota"
    ),  # Editar nota
    path(
        "eliminar/<int:pk>/", views.NotaDeleteView.as_view(), name="eliminar_nota"
    ),  # Eliminar nota
]
