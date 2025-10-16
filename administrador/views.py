from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import AdministradorForm


def listar_administradores(request):
    data = {
        "titulo": "Listado de Administradores",
        "administradores": Administrador.objects.all()
    }
    return render(request, 'modulos/administrador.html', data)


class AdministradorListView(ListView):
    model = Administrador
    template_name = 'modulos/administrador.html'
    context_object_name = 'administradores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Administradores'
        return context


class AdministradorCreateView(CreateView):
    model = Administrador
    template_name = 'forms/formulario_crear.html'
    form_class = AdministradorForm
    success_url = '/apps/administradores/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear administrador'
        context['modulo'] = "administrador"
        return context


class AdministradorUpdateView(UpdateView):
    model = Administrador
    template_name = 'forms/formulario_actualizacion.html'
    form_class = AdministradorForm
    success_url = '/apps/administradores/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/administradores/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Administrador'
        return context


from django.shortcuts import render

# Create your views here.
