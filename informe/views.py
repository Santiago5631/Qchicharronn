from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import *
from .forms import InformeForm


def listar_informes(request):
    data = {
        "titulo": "Listado de Informes",
        "informes": Informe.objects.all()
    }
    return render(request, 'modulos/informe.html', data)


class InformeListView(ListView):
    model = Informe
    template_name = 'modulos/informe.html'
    context_object_name = 'informes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Informes'
        return context


class InformeCreateView(CreateView):
    model = Informe
    template_name = 'forms/formulario_crear.html'
    fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin', 'creado_por']
    success_url = '/apps/informes/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Informe'
        context['modulo'] = "informe"
        return context


class InformeUpdateView(UpdateView):
    model = Informe
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin', 'creado_por']
    success_url = '/apps/informes/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class InformeDeleteView(DeleteView):
    model = Informe
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/informes/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Informe'
        return context


from django.shortcuts import render

# Create your views here.
