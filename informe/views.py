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

    # Encabezados exactamente como en la tabla HTML
    encabezados = [
        'Título',
        'Tipo',
        'Rango de Fechas',
        'Creado Por',
        'Fecha de Creación'
    ]
    ws.append(encabezados)

    # Todos los informes
    informes = Informe.objects.select_related('creado_por').all()

    for informe in informes:
        rango_fechas = ""
        if informe.fecha_inicio and informe.fecha_fin:
            rango_fechas = f"{informe.fecha_inicio.strftime('%d/%m/%Y')} a {informe.fecha_fin.strftime('%d/%m/%Y')}"
        elif informe.fecha_inicio:
            rango_fechas = f"Desde {informe.fecha_inicio.strftime('%d/%m/%Y')}"
        elif informe.fecha_fin:
            rango_fechas = f"Hasta {informe.fecha_fin.strftime('%d/%m/%Y')}"

        fila = [
            informe.titulo or '',
            informe.get_tipo_display(),  # ← Aquí usamos el display del choice
            rango_fechas,
            informe.creado_por.username if informe.creado_por else 'N/A',
            informe.fecha_creacion.strftime('%d/%m/%Y %H:%M') if informe.fecha_creacion else '',
        ]
        ws.append(fila)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="informes.xlsx"'
    wb.save(response)
    return response


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def exportar_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph("Listado de Informes", styles['Title']))
    elements.append(Spacer(1, 20))

    # Datos
    data = [['Título', 'Tipo', 'Rango de Fechas', 'Creado Por', 'Fecha de Creación']]

    informes = Informe.objects.select_related('creado_por').all()

    for informe in informes:
        rango = ""
        if informe.fecha_inicio and informe.fecha_fin:
            rango = f"{informe.fecha_inicio.strftime('%d/%m/%Y')} a {informe.fecha_fin.strftime('%d/%m/%Y')}"
        elif informe.fecha_inicio:
            rango = f"Desde {informe.fecha_inicio.strftime('%d/%m/%Y')}"
        elif informe.fecha_fin:
            rango = f"Hasta {informe.fecha_fin.strftime('%d/%m/%Y')}"

        data.append([
            informe.titulo or '',
            informe.get_tipo_display(),
            rango,
            informe.creado_por.username if informe.creado_por else 'N/A',
            informe.fecha_creacion.strftime('%d/%m/%Y %H:%M') if informe.fecha_creacion else '',
        ])

    # Tabla con estilo bonito
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informes.pdf"'
    return response
# Create your views here.
