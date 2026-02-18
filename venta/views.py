from django.views.generic import ListView
from .models import Venta
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from clientes.models import Cliente


class VentaListView(ListView):
    model = Venta
    template_name = 'modulos/venta.html'
    context_object_name = 'ventas'
    ordering = ['-fecha_venta']  # más recientes primero

    def get_queryset(self):
        # optimización (no rompe nada)
        return Venta.objects.select_related('pedido').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔹 Separar ventas
        context['ventas_pendientes'] = self.object_list.filter(estado='pendiente')
        context['ventas_pagadas'] = self.object_list.filter(estado='pagado')

        context['titulo'] = 'Listado de Ventas'
        return context


class VentaDetailView(DetailView):
    model = Venta
    template_name = 'forms/venta_detalle.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        context['clientes'] = Cliente.objects.all()
        context['titulo'] = f'Detalle de Venta #{self.object.numero_factura}'
        return context



class VentaFacturaView(DetailView):
    model = Venta
    template_name = 'forms/factura.html'
    context_object_name = 'venta'

    def get_queryset(self):
        return Venta.objects.select_related(
            'pedido',
            'mesa'
        ).prefetch_related(
            'items'
        )

    def get_object(self, queryset=None):
        venta = super().get_object(queryset)
        if venta.estado != 'pagado':
            raise Http404("La venta aún no está pagada")
        return venta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        venta = self.object
        if not venta.cliente_factura and venta.cliente:
            context['cliente_factura_display'] = venta.cliente
        else:
            context['cliente_factura_display'] = venta.cliente_factura
        context['titulo'] = f'Factura {venta.numero_factura}'
        context['items'] = venta.items.all()
        context['fecha'] = venta.fecha_venta
        context['metodo_pago'] = venta.get_metodo_pago_display()
        context['clientes'] = Cliente.objects.all()

        print("ENTRANDO A VENTA FACTURA VIEW")
        print("Clientes:", Cliente.objects.count())

        return context



class VentaFinalizarView(View):
    def post(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)

        if venta.estado == 'pagado':
            messages.warning(request, 'Esta venta ya está finalizada.')
            return redirect('apl:venta:venta_list')

        # Obtener método de pago
        metodo_pago = request.POST.get('metodo_pago')
        if not metodo_pago:
            messages.error(request, 'Debe seleccionar un método de pago.')
            return redirect('apl:venta:venta_detail', pk=venta.pk)

        # ASIGNACIÓN AUTOMÁTICA DEL CLIENTE PARA FACTURACIÓN
        # Prioridad: si ya hay cliente_factura → mantenerlo
        # Si no, usar el del pedido si existe, o el nombre histórico
        if not venta.cliente_factura:
            if venta.cliente:
                venta.cliente_factura = venta.cliente
            elif venta.cliente_nombre:
                # Si solo tienes nombre, no puedes asignar objeto → opcional: dejar como está o crear un cliente genérico
                pass  # o manejar como prefieras

        # Guardar datos
        venta.metodo_pago = metodo_pago
        venta.estado = 'pagado'
        venta.save()

        # Marcar pedido como entregado (ya lo tienes)
        if venta.pedido:
            venta.pedido.estado = 'entregado'  # o 'terminado' como usas en services
            venta.pedido.save()

        messages.success(
            request,
            f'Venta #{venta.numero_factura} finalizada correctamente.'
        )

        return redirect('apl:venta:venta_factura', pk=venta.pk)


class VentaCambiarClienteView(View):
    def post(self, request, pk):
        print("=== CAMBIO CLIENTE EJECUTADO ===")
        print("Venta PK:", pk)
        print("POST completo:", request.POST)
        print("Método:", request.method)

        cliente_id = request.POST.get("cliente")
        print("Valor recibido de 'cliente':", cliente_id)

        venta = get_object_or_404(Venta, pk=pk)
        print("Cliente factura antes:", venta.cliente_factura_id)

        if cliente_id and cliente_id.strip() and cliente_id.isdigit():
            try:
                cliente = Cliente.objects.get(id=int(cliente_id))
                print("Cliente encontrado:", cliente.id, cliente.nombre)

                venta.cliente_factura = cliente
                venta.cliente_nombre = f"{cliente.nombre}"
                if cliente.numero_documento:
                    venta.cliente_nombre += f" - {cliente.numero_documento}"

                venta.save()
                print("Guardado OK → cliente_factura ahora:", venta.cliente_factura_id)
                messages.success(request, f"Cliente cambiado a {cliente.nombre}")
            except Cliente.DoesNotExist:
                print("Cliente NO existe con id:", cliente_id)
                messages.error(request, "Cliente no encontrado")
            except Exception as e:
                print("ERROR al guardar:", str(e))
                messages.error(request, f"Error: {str(e)}")
        else:
            print("No llegó cliente_id válido (vacío o no numérico)")
            messages.warning(request, "Selecciona un cliente válido")

        print("=== FIN CAMBIO ===")
        return redirect('apl:venta:venta_factura', pk=venta.pk)
