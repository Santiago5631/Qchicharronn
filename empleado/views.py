from django.shortcuts import render
from empleado.models import *
from django.views.generic import *


def listar_empleados(request):
    data = {
        "empleados": "empleados",
        "titulo": "Listado de Empleados",
        "empleado": Empleado.objects.all()
    }
    return render(request, 'modulos/empleado.html', data)


class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'modulos/empleado.html'
    context_object_name = 'empleados'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Empleados'
        return context


class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'forms/formulario_crear.html'
    fields = ['fecha_ingreso', 'estado', 'usuario']
    success_url = '/apps/empleados/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Empleado'
        context['modulo'] = "empleado"
        return context


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['nombre', 'apellido', 'cargo', 'salario']
    success_url = '/apps/empleados/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/empleados/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Empleado'
        return context