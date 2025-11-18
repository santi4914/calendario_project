# notas/views.py
import calendar
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Nota
from .forms import NotaForm # Lo crearemos en el siguiente paso

class CalendarioView(TemplateView):
    """
    Vista principal que muestra un calendario mensual.
    Permite navegar entre meses y muestra las notas asociadas a cada día.
    """
    template_name = "notas/calendario.html"

    def get_context_data(self, **kwargs):
        """
        Inyecta el contexto del calendario (mes, año, días, notas) en la plantilla.
        """
        context = super().get_context_data(**kwargs)

        # Obtiene el año y mes de la URL o usa la fecha actual
        year = self.kwargs.get("year", date.today().year)
        month = self.kwargs.get("month", date.today().month)

        # Crea una instancia de calendario y obtiene los días del mes
        cal = calendar.Calendar()
        month_days = cal.monthdatescalendar(year, month)

        current_date_obj = date(year, month, 1) # Objeto fecha para el mes actual

        # Lógica para navegación entre meses
        prev_month = current_date_obj - timedelta(days=1)
        next_month = current_date_obj + timedelta(days=32) # Suma 32 para asegurar el salto al siguiente mes

        context["month_days"] = month_days # Lista de semanas, cada una con una lista de objetos date
        context["current_date"] = current_date_obj
        context["prev_month_year"] = prev_month.year
        context["prev_month"] = prev_month.month
        context["next_month_year"] = next_month.year
        context["next_month"] = next_month.month
        context["current_month_name"] = current_date_obj.strftime("%B").capitalize() # Nombre del mes

        # Obtener todas las notas para el mes actual
        # Filtrar notas que caen dentro del rango del mes mostrado
        first_day_of_month = date(year, month, 1)
        last_day_of_month = date(year, month, calendar.monthrange(year, month)[1])
        
        # También obtener notas para los días de la semana anterior/siguiente que se muestran en el calendario
        first_day_shown = month_days[0][0] # Primer día de la primera semana mostrada
        last_day_shown = month_days[-1][-1] # Último día de la última semana mostrada

        notes_in_month = Nota.objects.filter(
            fecha__range=(first_day_shown, last_day_shown)
        ).order_by('fecha')

        # Organiza las notas por día para fácil acceso en la plantilla
        notes_by_day = {}
        for note in notes_in_month:
            notes_by_day.setdefault(note.fecha, []).append(note)
        
        context["notes_by_day"] = notes_by_day

        return context

# --- Vistas para CRUD de Notas ---

class NotaCreateView(CreateView):
    """
    Vista para crear una nueva nota.
    Pre-llena la fecha si se especifica en la URL.
    """
    model = Nota
    form_class = NotaForm # Usa un formulario que definiremos
    template_name = "notas/nota_form.html"

    def get_initial(self):
        """
        Establece valores iniciales para el formulario, como la fecha.
        """
        initial = super().get_initial()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            try:
                initial['fecha'] = date(year, month, day)
            except ValueError:
                pass # Si la fecha es inválida, no la pre-llena
        return initial

    def get_success_url(self):
        """
        Define a dónde redirigir después de crear una nota con éxito.
        Redirige al calendario del mes de la nota.
        """
        nota = self.object
        return reverse_lazy('notas:calendario_mes', kwargs={'year': nota.fecha.year, 'month': nota.fecha.month})

class NotaDetailView(DetailView):
    """
    Vista para mostrar los detalles de una nota específica.
    """
    model = Nota
    template_name = "notas/nota_detail.html"
    context_object_name = "nota" # Nombre de la variable en la plantilla

class NotaUpdateView(UpdateView):
    """
    Vista para editar una nota existente.
    """
    model = Nota
    form_class = NotaForm
    template_name = "notas/nota_form.html"

    def get_success_url(self):
        """
        Redirige al detalle de la nota después de la edición.
        """
        nota = self.object
        return reverse_lazy('notas:detalle_nota', kwargs={'pk': nota.pk})

class NotaDeleteView(DeleteView):
    """
    Vista para eliminar una nota existente.
    """
    model = Nota
    template_name = "notas/nota_confirm_delete.html" # Crea esta plantilla para confirmar la eliminación
    success_url = reverse_lazy('notas:calendario') # Redirige al calendario principal después de eliminar
    
    def post(self, request, *args, **kwargs):
        # Obtener el objeto antes de eliminarlo para extraer la fecha
        self.object = self.get_object()
        fecha_nota = self.object.fecha
        success_url = reverse_lazy(
            'notas:calendario_mes', 
            kwargs={'year': fecha_nota.year, 'month': fecha_nota.month}
        )
        self.object.delete()
        return redirect(success_url)