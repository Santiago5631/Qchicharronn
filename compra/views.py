# compra/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import CompraForm
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import io

from usuario.permisos import RolRequeridoMixin, rol_requerido, SOLO_ADMIN


class CompraListView(RolRequeridoMixin, ListView):
    """Solo administradores pueden ver compras."""
    roles_permitidos = SOLO_ADMIN
    model = Compra
    template_name = 'modulos/compra.html'
    context_object_name = 'compras'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Compras'
        return context


class CompraCreateView(RolRequeridoMixin, CreateView):
    """Solo administradores pueden crear compras."""
    roles_permitidos = SOLO_ADMIN
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


class CompraUpdateView(RolRequeridoMixin, UpdateView):
    """Solo administradores pueden editar compras."""
    roles_permitidos = SOLO_ADMIN
    model = Compra
    template_name = 'forms/formulario_actualizacion.html'
    fields = ['producto', 'fecha', 'precio', 'proveedor', 'cantidad', 'unidad']
    success_url = '/apps/compras/listar/'

    def form_valid(self, form):
        return super().form_valid(form)


class CompraDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden eliminar compras."""
    roles_permitidos = SOLO_ADMIN
    model = Compra
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = '/apps/compras/listar/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Compra'
        return context


# ──────────────────────────────────────────────
# EXPORTAR A EXCEL — Solo administradores
# ──────────────────────────────────────────────
@rol_requerido(*SOLO_ADMIN)
def exportar_compras_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Compras"

    encabezados = ['ID', 'Producto', 'Fecha', 'Precio', 'Proveedor', 'Cantidad', 'Unidad']
    ws.append(encabezados)

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="007bff", end_color="007bff", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center")

    for col in range(1, len(encabezados) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center

    compras = Compra.objects.select_related('producto', 'proveedor').all().order_by('-fecha')
    total_precio = 0

    for c in compras:
        precio = c.precio or 0
        total_precio += precio
        ws.append([
            c.id_factura or '',
            c.producto.nombre if c.producto else 'Sin producto',
            c.fecha.strftime('%d/%m/%Y') if c.fecha else '',
            f"${precio:,.2f}",
            str(c.proveedor) if c.proveedor else 'Sin proveedor',
            c.cantidad or 0,
            str(c.unidad) if c.unidad else '',
        ])

    ws.append([])
    ws.append(['', '', '', f'Total General:', f"${total_precio:,.2f}", '', ''])

    for i in range(1, 8):
        ws.column_dimensions[get_column_letter(i)].width = 15
    ws.column_dimensions[get_column_letter(2)].width = 30

    filename = f"compras_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response


# ──────────────────────────────────────────────
# EXPORTAR A PDF — Solo administradores
# ──────────────────────────────────────────────
@rol_requerido(*SOLO_ADMIN)
def exportar_compras_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    titulo = Paragraph(
        f"Listado de Compras<br/><small>Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}</small>",
        styles['Title']
    )
    elements.append(titulo)
    elements.append(Spacer(1, 20))

    data = [['ID', 'Producto', 'Fecha', 'Precio', 'Proveedor', 'Cantidad', 'Unidad']]

    compras = Compra.objects.select_related('producto', 'proveedor').all().order_by('-fecha')
    total_precio = 0

    for c in compras:
        precio = c.precio or 0
        total_precio += precio
        data.append([
            c.id_factura or '-',
            c.producto.nombre if c.producto else 'Sin producto',
            c.fecha.strftime('%d/%m/%Y') if c.fecha else '-',
            f"${precio:,.2f}",
            str(c.proveedor) if c.proveedor else 'Sin proveedor',
            str(c.cantidad or ''),
            str(c.unidad or ''),
        ])

    data.append(['', '', 'TOTAL:', f"${total_precio:,.2f}", '', '', ''])

    table = Table(data, colWidths=[50, 120, 70, 70, 100, 60, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"compras_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response