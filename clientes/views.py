from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm


class ClienteListView(ListView):
    model = Cliente
    template_name = "modulos/lista_clientes.html"
    context_object_name = "clientes"
    ordering = ["-creado"]


from django.shortcuts import redirect

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "forms/formulario_actualizacion.html"
    success_url = reverse_lazy("apl:clientes:lista_clientes")

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse_lazy("apl:clientes:lista_clientes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context
