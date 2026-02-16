from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import datetime

from .models import Nomina
from .forms import NominaForm, NominaFiltroForm


class NominaListView(ListView):
    model = Nomina
    template_name = 'modulos/nomina.html'
    context_object_name = 'nominas'
    paginate_by = 20

    def get_queryset(self):
        queryset = Nomina.objects.select_related('empleado', 'creado_por').all()

        # Filtros
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        empleado_id = self.request.GET.get('empleado')
        estado = self.request.GET.get('estado')

        if fecha_inicio:
            queryset = queryset.filter(fecha_pago__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_pago__lte=fecha_fin)
        if empleado_id:
            queryset = queryset.filter(empleado_id=empleado_id)
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Nóminas'
        context['filtro_form'] = NominaFiltroForm(self.request.GET)

        # Calcular totales
        nominas = self.get_queryset()
        context['total_general'] = nominas.aggregate(total=Sum('total'))['total'] or 0
        context['total_pendiente'] = nominas.filter(estado='pendiente').aggregate(total=Sum('total'))['total'] or 0
        context['total_pagado'] = nominas.filter(estado='pagado').aggregate(total=Sum('total'))['total'] or 0

        return context


class NominaCreateView(CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'forms/formulario_crear.html'
    success_url = reverse_lazy('apl:nomina:nomina_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nómina'
        context['entidad'] = 'Nómina'
        return context

    def form_valid(self, form):
        # Asignar el usuario autenticado como creador solo si está autenticado
        if self.request.user.is_authenticated:
            form.instance.creado_por = self.request.user
        messages.success(self.request, 'Nómina creada correctamente')
        return super().form_valid(form)


class NominaUpdateView(UpdateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'forms/formulario_actualizacion.html'
    success_url = reverse_lazy('apl:nomina:nomina_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Nómina'
        context['entidad'] = 'Nómina'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Nómina actualizada correctamente')
        return super().form_valid(form)


class NominaDeleteView(DeleteView):
    model = Nomina
    success_url = reverse_lazy('apl:nomina:nomina_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


def generar_pdf_nomina(request):
    """Genera un PDF con el reporte de nóminas filtrado"""

    # Obtener filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    empleado_id = request.GET.get('empleado')
    estado = request.GET.get('estado')

    # Filtrar nóminas
    nominas = Nomina.objects.select_related('empleado').all()

    if fecha_inicio:
        nominas = nominas.filter(fecha_pago__gte=fecha_inicio)
    if fecha_fin:
        nominas = nominas.filter(fecha_pago__lte=fecha_fin)
    if empleado_id:
        nominas = nominas.filter(empleado_id=empleado_id)
    if estado:
        nominas = nominas.filter(estado=estado)

    # Calcular totales
    total_general = nominas.aggregate(total=Sum('total'))['total'] or 0

    # Contexto para el template
    context = {
        'nominas': nominas,
        'total_general': total_general,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'fecha_generacion': datetime.datetime.now(),
    }

    # Renderizar template
    template = get_template('nomina/reporte_pdf.html')
    html = template.render(context)

    # Crear PDF
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment; filename="reporte_nomina_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'

    # Generar PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response
