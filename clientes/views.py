from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm


class ClienteListView(ListView):
    model = Cliente
    template_name = "modulos/lista_clientes.html"
    context_object_name = "clientes"
    ordering = ["-creado"]


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "forms/formulario_actualizacion.html"
    success_url = reverse_lazy("apl:clientes:lista_clientes")
