from django.views.generic import ListView
from .models import Venta
from django.http import Http404

class VentaListView(ListView):
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'
    ordering = ['fecha_venta']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        return context
from django.views.generic import DetailView

class VentaDetailView(DetailView):
    model = Venta
    template_name = 'forms/venta_detalle.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Detalle de Venta #{self.object.numero_factura}'
        return context


class VentaFacturaView(DetailView):
    model = Venta
    template_name = 'ventas/factura.html'
    context_object_name = 'venta'

    def get_object(self, queryset=None):
        venta = super().get_object(queryset)
        if venta.estado != 'pagado':
            raise Http404("La venta aún no está pagada")
        return venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Factura {self.object.numero_factura}'
        return context

