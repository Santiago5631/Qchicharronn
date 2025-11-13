from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import *
from .forms import InformeForm
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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

def exportar_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Informes"

    encabezados = ['Titulo', 'Descripcion', 'Tipo', 'Fecha inicio', 'Fecha fin', 'Creado por']
    ws.append(encabezados)

    informes = Informe.objects.all()
    for i in informes:
        ws.append([
            i.titulo,
            i.descripcion,
            i.tipo,
            i.fecha_inicio.strftime('%d/%m/%Y') if i.fecha_inicio else '',
            i.fecha_fin.strftime('%d/%m/%Y') if i.fecha_fin else '',
            i.creado_por.username if i.creado_por else '',
        ])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="informes.xlsx"'
    wb.save(response)
    return response

def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informes.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 770, "Informe General")
    p.setFont("Helvetica", 11)

    y = 740
    informes = Informe.objects.all()
    for i in informes:
        p.drawString(50, y, f"Titulo: {i.titulo}")
        y -= 15
        p.drawString(50, y, f"Descripcion: {i.descripcion[:80]}...")
        y -= 15
        p.drawString(50, y, f"Tipo: {i.tipo}")
        y -= 15
        p.drawString(50, y, f"Fecha inicio: {i.fecha_inicio} | Fecha fin: {i.fecha_fin}")
        y -= 15
        p.drawString(50, y, f"Creado por: {i.creado_por.username if i.creado_por else 'N/A'}")
        y -= 15

        if y < 100:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 11)

    p.save()
    return response
# Create your views here.
