# notas/forms.py
from django import forms
from .models import Nota


class NotaForm(forms.ModelForm):
    """
    Formulario para el modelo Nota.
    """

    # Puedes personalizar widgets aquí si quieres
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Fecha de la nota"
    )

    class Meta:
        model = Nota
        fields = ["titulo", "contenido", "fecha"]
        labels = {
            "titulo": "Título de la Nota",
            "contenido": "Descripción",
        }
        # No incluir 'fecha_creacion' ya que se genera automáticamente
