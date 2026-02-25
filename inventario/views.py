# inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal

from .models import InventarioDiario, MovimientoInventario, HistorialStock, TipoInventario
from .forms import (
    AperturaInventarioForm,
    MovimientoInventarioFormSet,
    CierreInventarioFormSet,
    AjusteInventarioForm,
    FiltroReporteForm
)
from producto.models import Producto

from usuario.permisos import RolRequeridoMixin, COCINAS
# COCINAS = ['administrador', 'cocinero', 'parrilla']
# Los meseros NO tienen acceso al inventario


# ==================== DASHBOARD ====================
class InventarioDashboardView(RolRequeridoMixin, View):
    """Vista principal del inventario — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    template_name = 'inventario/dashboard.html'

    def get(self, request):
        hoy = timezone.now().date()
        inventario_hoy = InventarioDiario.objects.filter(fecha=hoy).first()

        productos_bajo_stock = Producto.objects.filter(
            disponible=True,
            stock__lt=10
        ).order_by('stock')[:10]

        ultimos_movimientos = MovimientoInventario.objects.select_related(
            'producto', 'inventario_diario'
        ).order_by('-fecha_actualizacion')[:10]

        productos_sin_stock = Producto.objects.filter(
            disponible=True,
            stock=0
        ).count()

        context = {
            'titulo': 'Dashboard de Inventario',
            'inventario_hoy': inventario_hoy,
            'productos_bajo_stock': productos_bajo_stock,
            'ultimos_movimientos': ultimos_movimientos,
            'productos_sin_stock': productos_sin_stock,
        }
        return render(request, self.template_name, context)


# ==================== APERTURA DE INVENTARIO ====================
class AperturaInventarioView(RolRequeridoMixin, View):
    """Abrir inventario del día — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    template_name = 'inventario/apertura.html'

    def get(self, request):
        hoy = timezone.now().date()

        if InventarioDiario.objects.filter(fecha=hoy).exists():
            messages.warning(request, 'Ya existe un inventario abierto para hoy')
            return redirect('apl:inventario:dashboard')

        form = AperturaInventarioForm(initial={'fecha': hoy})
        productos = Producto.objects.filter(disponible=True).order_by('nombre')

        context = {
            'titulo': 'Apertura de Inventario',
            'form': form,
            'productos': productos,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AperturaInventarioForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    inventario = form.save()

                    productos_data = {}
                    for key, value in request.POST.items():
                        if key.startswith('producto_'):
                            producto_id = key.split('_')[1]
                            if value.strip():
                                productos_data[producto_id] = value

                    if not productos_data:
                        messages.error(request, 'Debe seleccionar al menos un producto')
                        return redirect('apl:inventario:apertura')

                    for producto_id, inventario_inicial in productos_data.items():
                        producto = Producto.objects.get(id=producto_id)
                        MovimientoInventario.objects.create(
                            inventario_diario=inventario,
                            producto=producto,
                            tipo_control=producto.tipo_inventario,
                            inventario_inicial=Decimal(inventario_inicial),
                        )
                        producto.stock = Decimal(inventario_inicial)
                        producto.save()

                    messages.success(
                        request,
                        f'Inventario abierto exitosamente con {len(productos_data)} productos'
                    )
                    return redirect('apl:inventario:detalle', pk=inventario.pk)

            except Exception as e:
                messages.error(request, f'Error al abrir inventario: {str(e)}')
                return redirect('apl:inventario:apertura')
        else:
            messages.error(request, 'Por favor corrija los errores')
            return self.get(request)


# ==================== CIERRE DE INVENTARIO ====================
class CierreInventarioView(RolRequeridoMixin, View):
    """Cerrar inventario del día — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    template_name = 'inventario/cierre.html'

    def get(self, request, pk):
        inventario = get_object_or_404(InventarioDiario, pk=pk)

        if inventario.estado == 'cerrado':
            messages.warning(request, 'Este inventario ya está cerrado')
            return redirect('apl:inventario:detalle', pk=pk)

        movimientos = inventario.movimientos.select_related('producto').order_by('producto__nombre')

        context = {
            'titulo': 'Cierre de Inventario',
            'inventario': inventario,
            'movimientos': movimientos,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        inventario = get_object_or_404(InventarioDiario, pk=pk)

        if inventario.estado == 'cerrado':
            messages.error(request, 'Este inventario ya está cerrado')
            return redirect('apl:inventario:detalle', pk=pk)

        try:
            with transaction.atomic():
                movimientos = inventario.movimientos.all()
                registros_procesados = 0

                for movimiento in movimientos:
                    campo_nombre  = f'inventario_final_{movimiento.id}'
                    motivo_nombre = f'motivo_ajuste_{movimiento.id}'
                    inventario_final = request.POST.get(campo_nombre)
                    motivo_ajuste    = request.POST.get(motivo_nombre, '')

                    if inventario_final:
                        movimiento.registrar_cierre(
                            inventario_final_fisico=inventario_final,
                            motivo_ajuste=motivo_ajuste if motivo_ajuste else None
                        )
                        HistorialStock.objects.create(
                            producto=movimiento.producto,
                            tipo_movimiento='cierre',
                            cantidad=movimiento.consumo_calculado,
                            stock_anterior=movimiento.inventario_inicial,
                            stock_nuevo=movimiento.inventario_final,
                            referencia=f"Cierre {inventario.fecha.strftime('%d/%m/%Y')}",
                            observaciones=f"Consumo: {movimiento.consumo_calculado} | Ajuste: {movimiento.ajuste_manual}"
                        )
                        registros_procesados += 1

                inventario.cerrar_inventario()
                messages.success(
                    request,
                    f'Inventario cerrado exitosamente. {registros_procesados} productos procesados'
                )
                return redirect('apl:inventario:detalle', pk=pk)

        except Exception as e:
            messages.error(request, f'Error al cerrar inventario: {str(e)}')
            return redirect('apl:inventario:cierre', pk=pk)


# ==================== DETALLE DE INVENTARIO ====================
class InventarioDetalleView(RolRequeridoMixin, DetailView):
    """Detalle de inventario — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    model = InventarioDiario
    template_name = 'inventario/detalle.html'
    context_object_name = 'inventario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Inventario {self.object.fecha.strftime('%d/%m/%Y')}"

        movimientos = self.object.movimientos.select_related('producto').order_by('producto__nombre')
        context['movimientos_peso']   = movimientos.filter(tipo_control='peso')
        context['movimientos_unidad'] = movimientos.filter(tipo_control='unidad')

        total_productos = movimientos.count()
        productos_con_diferencia = movimientos.exclude(
            inventario_final__isnull=True
        ).filter(tipo_control='unidad').exclude(ajuste_manual=0).count()

        context['total_productos']         = total_productos
        context['productos_con_diferencia'] = productos_con_diferencia
        return context


# ==================== LISTA DE INVENTARIOS ====================
class InventarioListView(RolRequeridoMixin, ListView):
    """Lista de todos los inventarios — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    model = InventarioDiario
    template_name = 'inventario/lista.html'
    context_object_name = 'inventarios'
    paginate_by = 20

    def get_queryset(self):
        queryset = InventarioDiario.objects.all()
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']         = 'Lista de Inventarios'
        context['estado_actual']  = self.request.GET.get('estado', '')
        return context


# ==================== AJUSTES MANUALES ====================
class AjusteInventarioView(RolRequeridoMixin, View):
    """Ajustes manuales — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    template_name = 'inventario/ajuste.html'

    def get(self, request):
        form = AjusteInventarioForm()
        context = {
            'titulo': 'Ajuste Manual de Inventario',
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AjusteInventarioForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    producto         = form.cleaned_data['producto']
                    tipo_movimiento  = form.cleaned_data['tipo_movimiento']
                    cantidad         = form.cleaned_data['cantidad']
                    motivo           = form.cleaned_data['motivo']
                    stock_anterior   = producto.stock

                    if tipo_movimiento == 'entrada':
                        producto.stock += cantidad
                    elif tipo_movimiento == 'salida':
                        producto.stock -= cantidad
                    elif tipo_movimiento == 'ajuste':
                        producto.stock = cantidad

                    producto.save()

                    HistorialStock.objects.create(
                        producto=producto,
                        tipo_movimiento=tipo_movimiento,
                        cantidad=cantidad,
                        stock_anterior=stock_anterior,
                        stock_nuevo=producto.stock,
                        referencia='Ajuste Manual',
                        observaciones=motivo
                    )

                    messages.success(
                        request,
                        f'Ajuste realizado: {producto.nombre} - Stock: {stock_anterior} → {producto.stock}'
                    )
                    return redirect('apl:inventario:dashboard')

            except Exception as e:
                messages.error(request, f'Error al realizar ajuste: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores')

        return self.get(request)


# ==================== REPORTES ====================
class ReporteInventarioView(RolRequeridoMixin, View):
    """Reportes de inventario — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    template_name = 'inventario/reporte.html'

    def get(self, request):
        form = FiltroReporteForm(request.GET or None)
        movimientos  = None
        estadisticas = {}

        if form.is_valid():
            movimientos = MovimientoInventario.objects.select_related(
                'producto', 'inventario_diario'
            ).exclude(inventario_final__isnull=True)

            fecha_desde  = form.cleaned_data.get('fecha_desde')
            fecha_hasta  = form.cleaned_data.get('fecha_hasta')
            producto     = form.cleaned_data.get('producto')
            tipo_control = form.cleaned_data.get('tipo_control')

            if fecha_desde:
                movimientos = movimientos.filter(inventario_diario__fecha__gte=fecha_desde)
            if fecha_hasta:
                movimientos = movimientos.filter(inventario_diario__fecha__lte=fecha_hasta)
            if producto:
                movimientos = movimientos.filter(producto=producto)
            if tipo_control:
                movimientos = movimientos.filter(tipo_control=tipo_control)

            movimientos = movimientos.order_by('-inventario_diario__fecha')

            if movimientos.exists():
                estadisticas = {
                    'total_registros': movimientos.count(),
                    'total_consumo': sum(m.consumo_calculado for m in movimientos),
                    'total_diferencias': sum(abs(m.diferencia) for m in movimientos),
                    'productos_con_ajuste': movimientos.exclude(ajuste_manual=0).count(),
                }

        context = {
            'titulo': 'Reporte de Inventario',
            'form': form,
            'movimientos': movimientos,
            'estadisticas': estadisticas,
        }
        return render(request, self.template_name, context)


# ==================== HISTORIAL DE STOCK ====================
class HistorialStockView(RolRequeridoMixin, ListView):
    """Historial de stock — Admin, Cocinero, Parrilla."""
    roles_permitidos = COCINAS
    model = HistorialStock
    template_name = 'inventario/historial.html'
    context_object_name = 'movimientos'
    paginate_by = 50

    def get_queryset(self):
        queryset = HistorialStock.objects.select_related('producto')
        producto_id = self.request.GET.get('producto')
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        return queryset.order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']               = 'Historial de Stock'
        context['productos']            = Producto.objects.filter(disponible=True)
        context['producto_seleccionado'] = self.request.GET.get('producto', '')
        return context