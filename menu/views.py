from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from .forms import *
from .models import Menu, MenuProducto, Pedido, PedidoItem
from decimal import Decimal


# ==================== VISTAS DE MENÚ ====================

class MenuListView(ListView):
    """Lista de menús disponibles"""
    model = Menu
    template_name = 'modulos/menu.html'
    context_object_name = 'menus'

    def get_queryset(self):
        return Menu.objects.prefetch_related('menu_productos__producto').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Menús'
        context['menu'] = 'menu'
        return context


class MenuCreateView(CreateView):
    """Crear nuevo menú"""
    model = Menu
    template_name = 'forms/forms_menu_crear.html'
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Menú'
        context['title'] = 'Crear Nuevo Menú'
        context['modulo'] = "menu"

        if self.request.POST:
            context['formset'] = MenuProductoFormSet(
                self.request.POST,
                prefix='menu_productos'
            )
        else:
            context['formset'] = MenuProductoFormSet(
                prefix='menu_productos',
                queryset=MenuProducto.objects.none()
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        try:
            with transaction.atomic():
                # Validar formset
                if not formset.is_valid():
                    messages.error(self.request, 'Hay errores en los productos seleccionados.')
                    return self.form_invalid(form)

                # Verificar que hay al menos un producto
                productos_validos = [
                    f for f in formset.cleaned_data
                    if f and not f.get('DELETE', False)
                ]

                if not productos_validos:
                    messages.error(
                        self.request,
                        'Debe agregar al menos un producto al menú.'
                    )
                    return self.form_invalid(form)

                # Guardar el menú
                self.object = form.save()

                # Guardar los productos
                formset.instance = self.object
                formset.save()

                messages.success(
                    self.request,
                    f'Menú "{self.object.nombre}" creado exitosamente con {len(productos_validos)} producto(s).'
                )
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f'Error al crear el menú: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


class MenuUpdateView(UpdateView):
    """Actualizar menú existente"""
    model = Menu
    template_name = 'forms/forms_menu_crear.html'
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Menú'
        context['title'] = 'Actualizar Menú'
        context['modulo'] = "menu"

        if self.request.POST:
            context['formset'] = MenuProductoFormSet(
                self.request.POST,
                instance=self.object,
                prefix='menu_productos'
            )
        else:
            context['formset'] = MenuProductoFormSet(
                instance=self.object,
                prefix='menu_productos'
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        try:
            with transaction.atomic():
                if not formset.is_valid():
                    messages.error(self.request, 'Hay errores en los productos.')
                    return self.form_invalid(form)

                productos_validos = [
                    f for f in formset.cleaned_data
                    if f and not f.get('DELETE', False)
                ]

                if not productos_validos:
                    messages.error(self.request, 'Debe tener al menos un producto.')
                    return self.form_invalid(form)

                self.object = form.save()
                formset.instance = self.object
                formset.save()

                messages.success(
                    self.request,
                    f'Menú "{self.object.nombre}" actualizado exitosamente.'
                )
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f'Error al actualizar: {str(e)}')
            return self.form_invalid(form)


class MenuDeleteView(DeleteView):
    """Eliminar menú"""
    model = Menu
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:menu:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Menú'
        return context

    def delete(self, request, *args, **kwargs):
        menu = self.get_object()
        nombre = menu.nombre

        # Si es AJAX (SweetAlert), devolver JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            menu.delete()
            return JsonResponse({'success': True, 'nombre': nombre})

        # Si no es AJAX, eliminar y redirigir normalmente
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Menú "{nombre}" eliminado exitosamente.')
        return response


@require_POST
def menu_delete_ajax(request, pk):
    """Vista auxiliar para eliminar con AJAX"""
    try:
        menu = get_object_or_404(Menu, pk=pk)
        nombre = menu.nombre
        menu.delete()
        return JsonResponse({'success': True, 'nombre': nombre})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


class MenuDetailView(DetailView):
    """Ver detalle de un menú con sus productos"""
    model = Menu
    template_name = 'forms/menu_detalle.html'
    context_object_name = 'menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Detalle: {self.object.nombre}'
        context['productos'] = self.object.menu_productos.select_related('producto').all()
        return context


# ==================== VISTAS DE PEDIDOS ====================
class PedidoListView( ListView):
    model = Pedido
    template_name = 'forms/pedido_lista.html'  # ← CORREGIDO: nombre real del template
    context_object_name = 'pedidos'
    paginate_by = 12  # ← 12 queda más bonito en tarjetas
    ordering = ['-fecha_creacion']  # ← más nuevos primero

    def get_queryset(self):
        queryset = Pedido.objects.prefetch_related('items__menu').all()

        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            # Validamos que el estado sea válido
            if estado in dict(Pedido.ESTADO_CHOICES):  # ← USA .ESTADOS (no ESTADO_CHOICES)
                queryset = queryset.filter(estado=estado)

        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Pedidos'
        context['menu'] = 'pedido'

        # ← CORREGIDO: usar Pedido.ESTADOS (el choices de tu modelo)
        context['estados'] = Pedido.ESTADO_CHOICES

        # Para resaltar el filtro activo
        context['estado_actual'] = self.request.GET.get('estado', '')

        # Estadísticas reales (opcional pero queda brutal)
        context['stats'] = {
            'total': Pedido.objects.count(),
            'pendiente': Pedido.objects.filter(estado='pendiente').count(),
            'preparando': Pedido.objects.filter(estado='preparando').count(),
            'listo': Pedido.objects.filter(estado='listo').count(),
            'entregado': Pedido.objects.filter(estado='entregado').count(),
            'cancelado': Pedido.objects.filter(estado='cancelado').count(),
        }

        return context

class PedidoCreateView(View):
    template_name = 'forms/pedido_crear.html'

    def get(self, request, *args, **kwargs):
        return self._renderizar_pagina(request)

    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')

        # 1. Agregar al carrito
        if accion == 'agregar':
            menu_id = request.POST.get('menu_id')
            if not menu_id or not menu_id.isdigit():
                messages.error(request, 'Menú no válido.')
                return redirect('apl:menu:pedido_create')

            cantidad = int(request.POST.get('cantidad', 1))
            observaciones = request.POST.get('observaciones', '').strip()

            carrito = request.session.get('carrito', {})
            if menu_id in carrito:
                carrito[menu_id]['cantidad'] += cantidad
            else:
                carrito[menu_id] = {'cantidad': cantidad, 'observaciones': observaciones}

            request.session['carrito'] = carrito
            request.session.modified = True
            messages.success(request, 'Producto agregado al carrito')
            return redirect('apl:menu:pedido_create')

        # 2. Actualizar cantidad
        elif accion == 'actualizar':
            menu_id = request.POST.get('menu_id')
            if menu_id and menu_id.isdigit():
                cantidad = max(int(request.POST.get('cantidad', 1)), 1)
                carrito = request.session.get('carrito', {})
                if menu_id in carrito:
                    carrito[menu_id]['cantidad'] = cantidad
                    request.session['carrito'] = carrito
                    request.session.modified = True
            return redirect('apl:menu:pedido_create')

        # 3. Eliminar del carrito
        elif accion == 'eliminar':
            menu_id = request.POST.get('menu_id')
            carrito = request.session.get('carrito', {})
            carrito.pop(menu_id, None)
            request.session['carrito'] = carrito
            request.session.modified = True
            messages.info(request, 'Producto eliminado del carrito')
            return redirect('apl:menu:pedido_create')

        # 4. Confirmar pedido
        elif accion == 'confirmar':
            form = PedidoForm(request.POST)
            if form.is_valid():
                carrito = request.session.get('carrito', {})
                if not carrito:
                    messages.error(request, 'El carrito está vacío.')
                    return self._renderizar_pagina(request, form=form)
                pedido = form.save(commit=False)  # ← Aquí creas el objeto pero NO lo guardas aún
                pedido.estado = 'pendiente'  # ← ¡¡AQUÍ LE ASIGNAS EL ESTADO!!
                pedido.save()
                try:
                    with transaction.atomic():
                        pedido = form.save(commit=False)
                        pedido.save()

                        for menu_id_str, datos in carrito.items():
                            if not menu_id_str.isdigit():
                                continue
                            menu = get_object_or_404(Menu, id=int(menu_id_str))
                            PedidoItem.objects.create(
                                pedido=pedido,
                                menu=menu,
                                cantidad=datos.get('cantidad', 1),
                                precio_unitario=menu.get_precio_final(),
                                descuento_aplicado=menu.descuento or 0,
                                observaciones=datos.get('observaciones', '')
                            )

                        pedido.calcular_totales()
                        request.session['carrito'] = {}
                        request.session.modified = True

                        messages.success(
                            request,
                            f'Pedido #{pedido.numero_pedido} creado exitosamente. Total: ${pedido.total}'
                        )
                        return redirect('apl:menu:pedido_detail', pk=pedido.pk)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    messages.error(request, f'Error al crear el pedido: {str(e)}')
                    return self._renderizar_pagina(request, form=form)

            else:
                messages.error(request, 'Corrige los errores en los datos del cliente.')
                return self._renderizar_pagina(request, form=form)

        # ← SIEMPRE devolver algo aunque no haya acción válida
        return redirect('apl:menu:pedido_create')

    # =============================================
    # Método auxiliar (nunca devuelve None)
    # =============================================
    def _renderizar_pagina(self, request, form=None):
        carrito = request.session.get('carrito', {})

        # Limpieza automática de claves basura
        carrito_limpio = {k: v for k, v in carrito.items() if k and str(k).isdigit()}
        if carrito_limpio != carrito:
            request.session['carrito'] = carrito_limpio
            request.session.modified = True
            carrito = carrito_limpio

        # Menús por categoría
        menus_por_categoria = {}
        for menu in Menu.objects.filter(disponible=True).prefetch_related('menu_productos__producto'):
            cat = menu.get_categoria_menu_display()
            menus_por_categoria.setdefault(cat, []).append(menu)

        # Cálculo de items del carrito
        items_carrito = []
        subtotal = Decimal('0.00')
        descuento_total = Decimal('0.00')

        for menu_id_str, datos in carrito.items():
            if not menu_id_str.isdigit():
                continue
            menu_id = int(menu_id_str)
            try:
                menu = Menu.objects.get(id=menu_id, disponible=True)
            except Menu.DoesNotExist:
                continue

            cantidad = datos.get('cantidad', 1)
            precio_final = menu.get_precio_final()
            subtotal_item = precio_final * cantidad

            items_carrito.append({
                'menu': menu,
                'cantidad': cantidad,
                'precio_unitario': precio_final,
                'subtotal': subtotal_item,
                'observaciones': datos.get('observaciones', '')
            })

            subtotal += subtotal_item
            if menu.descuento > 0:
                descuento_total += (menu.precio_base * cantidad) - subtotal_item

        context = {
            'titulo': 'Crear Nuevo Pedido',
            'menus_por_categoria': menus_por_categoria,
            'items_carrito': items_carrito,
            'subtotal': subtotal,
            'descuento_total': descuento_total,
            'total': subtotal,
            'form': form or PedidoForm(),
        }

        return render(request, self.template_name, context)
class PedidoDetailView(DetailView):
    """Ver detalle de un pedido"""
    model = Pedido
    template_name = 'forms/pedido_detalle.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Pedido #{self.object.numero_pedido}'
        context['items'] = self.object.items.select_related('menu').all()
        context['form_estado'] = ActualizarEstadoPedidoForm(instance=self.object)
        return context


class PedidoUpdateEstadoView(View):
    """Actualizar el estado de un pedido"""

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = ActualizarEstadoPedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()
            messages.success(request, f'Estado del pedido actualizado a: {pedido.get_estado_display()}')
        else:
            messages.error(request, 'Error al actualizar el estado')

        return redirect('apl:menu:pedido_detail', pk=pk)


class PedidoDeleteView(DeleteView):
    """Cancelar/eliminar pedido"""
    model = Pedido
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:menu:pedido_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cancelar Pedido'
        return context

    def delete(self, request, *args, **kwargs):
        pedido = self.get_object()
        numero = pedido.numero_pedido
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Pedido #{numero} cancelado exitosamente.')
        return response


# ==================== API AJAX ====================

class LimpiarCarritoView(View):
    """Limpiar todo el carrito"""

    def post(self, request):
        request.session['carrito'] = {}
        request.session.modified = True
        messages.info(request, 'Carrito limpiado')
        return redirect('apl:menu:pedido_create')