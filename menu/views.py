from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
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


class MenuDeleteView(View):
    """Eliminar menú - Acepta POST directo desde modal"""

    def post(self, request, pk):
        """Eliminar el menú directamente"""
        try:
            menu = get_object_or_404(Menu, pk=pk)
            nombre = menu.nombre

            # Eliminar el menú
            menu.delete()

            messages.success(
                request,
                f'✅ Menú "{nombre}" eliminado exitosamente.'
            )

        except Exception as e:
            messages.error(
                request,
                f'❌ Error al eliminar el menú: {str(e)}'
            )

        return redirect('apl:menu:menu_list')

    def get(self, request, pk):
        """Mostrar página de confirmación (opcional)"""
        menu = get_object_or_404(Menu, pk=pk)

        context = {
            'titulo': 'Eliminar Menú',
            'object': menu,
        }

        return render(request, 'forms/eliminacion_menu.html', context)


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

class PedidoListView(ListView):
    """Lista de todos los pedidos"""
    model = Pedido
    template_name = 'forms/pedido_lista.html'
    context_object_name = 'pedidos'
    paginate_by = 20

    def get_queryset(self):
        queryset = Pedido.objects.prefetch_related('items__menu').all()

        # Filtrar por estado si se proporciona
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pedidos'
        context['menu'] = 'pedido'
        context['estados'] = Pedido.ESTADO_CHOICES
        context['estado_actual'] = self.request.GET.get('estado', '')
        return context


class PedidoCreateView(View):
    """Vista para crear pedidos - Sistema de carrito"""
    template_name = 'forms/pedido_crear.html'

    def get(self, request):
        # Obtener o crear carrito en sesión
        carrito = request.session.get('carrito', {})

        # Obtener menús disponibles agrupados por categoría
        menus_por_categoria = {}
        for menu in Menu.objects.filter(disponible=True).prefetch_related('menu_productos__producto'):
            categoria = menu.get_categoria_menu_display()
            if categoria not in menus_por_categoria:
                menus_por_categoria[categoria] = []
            menus_por_categoria[categoria].append(menu)

        # Calcular totales del carrito
        subtotal = Decimal('0.00')
        descuento_total = Decimal('0.00')
        items_carrito = []

        for menu_id, item_data in carrito.items():
            try:
                menu = Menu.objects.get(id=int(menu_id))
                cantidad = item_data['cantidad']
                precio_unitario = menu.get_precio_final()
                subtotal_item = precio_unitario * cantidad

                items_carrito.append({
                    'menu': menu,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal_item,
                    'observaciones': item_data.get('observaciones', '')
                })

                subtotal += subtotal_item
                if menu.descuento > 0:
                    descuento_total += (menu.precio_base * cantidad) - subtotal_item
            except Menu.DoesNotExist:
                continue

        total = subtotal

        context = {
            'titulo': 'Crear Nuevo Pedido',
            'menus_por_categoria': menus_por_categoria,
            'items_carrito': items_carrito,
            'subtotal': subtotal,
            'descuento_total': descuento_total,
            'total': total,
            'form': PedidoForm()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        accion = request.POST.get('accion')

        # Agregar al carrito
        if accion == 'agregar':
            menu_id = request.POST.get('menu_id')
            cantidad = int(request.POST.get('cantidad', 1))
            observaciones = request.POST.get('observaciones', '')

            carrito = request.session.get('carrito', {})

            if menu_id in carrito:
                carrito[menu_id]['cantidad'] += cantidad
            else:
                carrito[menu_id] = {
                    'cantidad': cantidad,
                    'observaciones': observaciones
                }

            request.session['carrito'] = carrito
            messages.success(request, 'Producto agregado al pedido')
            return redirect('apl:menu:pedido_create')

        # Actualizar cantidad
        elif accion == 'actualizar':
            menu_id = request.POST.get('menu_id')
            cantidad = int(request.POST.get('cantidad', 1))

            carrito = request.session.get('carrito', {})
            if menu_id in carrito:
                carrito[menu_id]['cantidad'] = cantidad
                request.session['carrito'] = carrito

            return redirect('apl:menu:pedido_create')

        # Eliminar del carrito
        elif accion == 'eliminar':
            menu_id = request.POST.get('menu_id')
            carrito = request.session.get('carrito', {})

            if menu_id in carrito:
                del carrito[menu_id]
                request.session['carrito'] = carrito
                messages.info(request, 'Producto eliminado del pedido')

            return redirect('apl:menu:pedido_create')

        # Confirmar pedido
        elif accion == 'confirmar':
            form = PedidoForm(request.POST)

            if form.is_valid():
                carrito = request.session.get('carrito', {})

                if not carrito:
                    messages.error(request, 'El carrito está vacío')
                    return redirect('apl:menu:pedido_create')

                try:
                    with transaction.atomic():
                        # Crear pedido
                        pedido = form.save(commit=False)
                        pedido.save()

                        # Crear items del pedido
                        for menu_id, item_data in carrito.items():
                            try:
                                menu = Menu.objects.get(id=int(menu_id))

                                PedidoItem.objects.create(
                                    pedido=pedido,
                                    menu=menu,
                                    cantidad=item_data['cantidad'],
                                    precio_unitario=menu.get_precio_final(),
                                    descuento_aplicado=menu.descuento,
                                    observaciones=item_data.get('observaciones', '')
                                )
                            except Menu.DoesNotExist:
                                continue

                        # Calcular totales
                        pedido.calcular_totales()

                        # Limpiar carrito
                        request.session['carrito'] = {}
                        request.session.modified = True

                        messages.success(
                            request,
                            f'✅ Pedido #{pedido.numero_pedido} creado exitosamente. Total: ${pedido.total}'
                        )
                        return redirect('apl:menu:pedido_detail', pk=pedido.pk)

                except Exception as e:
                    messages.error(request, f'Error al crear el pedido: {str(e)}')
                    return redirect('apl:menu:pedido_create')
            else:
                messages.error(request, 'Por favor complete los datos del cliente correctamente')
                return redirect('apl:menu:pedido_create')

        return redirect('apl:menu:pedido_create')


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
        messages.info(request, 'Carrito limpiado')
        return redirect('apl:menu:pedido_create')