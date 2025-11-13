from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import CompraForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from openpyxl import Workbook
from xhtml2pdf import pisa
import io


def listar_compras(request):
    data = {
        "titulo": "Listado de Compras",
        "compras": Compra.objects.all()
    }
    return render(request, 'modulos/compra.html', data)


class CompraListView(ListView):
    model = Compra
    template_name = 'modulos/compra.html'
    context_object_name = 'compras'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Compras'
        return context


class CompraCreateView(CreateView):
    model = Compra
    template_name = 'forms/formulario_crear.html'
    form_class = CompraForm
    success_url = '/apps/compras/listar/'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Compra'
        context['modulo'] = "compra"
        return context


class CompraUpdateView(UpdateView):
    model = Compra
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['producto', 'fecha', 'precio', 'proveedor', 'cantidad', 'unidad']
    success_url = '/apps/compras/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/compras/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Compra'
        return context


from django.shortcuts import render

# -------------------- EXPORTAR A EXCEL --------------------
def exportar_compras_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compras"
    ws.append(["ID", "Producto", "Fecha", "Precio", "Proveedor", "Cantidad", "Unidad"])

    for c in Compra.objects.all().order_by('-fecha'):
        ws.append([
            c.id_factura,
            c.producto.nombre if hasattr(c.producto, 'nombre') else str(c.producto),
            c.fecha.strftime('%Y-%m-%d'),
            c.precio,
            str(c.proveedor),
            c.cantidad,
            str(c.unidad)
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="compras_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    wb.save(response)
    return response


# -------------------- EXPORTAR A PDF --------------------
def exportar_compras_pdf(request):
    compras = Compra.objects.all().order_by('-fecha')
    html = render_to_string('modulos/compra_pdf.html', {
        'compras': compras,
        'titulo': 'Listado de Compras',
        'fecha_actual': timezone.now()  # Agrega esta línea
    })
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="compras_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    return response


# -------------------- FACTURA INDIVIDUAL --------------------
def generar_factura_pdf(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    html = render_to_string('modulos/factura_compra.html', {
        'compra': compra,
        'fecha_actual': timezone.now()
    })
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)
    if pisa_status.err:
        return HttpResponse("Error al generar la factura", status=500)
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_compra_{compra.id_factura}.pdf"'
    return response
# Create your views here.
