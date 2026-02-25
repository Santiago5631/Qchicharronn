# menu/views.py
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
from venta.services import crear_venta_desde_pedido, actualizar_venta_desde_pedido
from django.urls import reverse
from django.db.models import Count

from usuario.permisos import RolRequeridoMixin, rol_requerido, SOLO_ADMIN, TODOS, COCINAS


# ══════════════════════════════════════════════
# VISTAS DE MENÚ
# ══════════════════════════════════════════════

class MenuListView(RolRequeridoMixin, ListView):
    """
    Todos los roles pueden VER el menú.
    (Meseros lo necesitan para tomar pedidos, cocineros para saber qué preparan)
    """
    roles_permitidos = TODOS
    model = Menu
    template_name = 'modulos/menu.html'
    context_object_name = 'menus'

    def get_queryset(self):
        return Menu.objects.prefetch_related('menu_productos__producto').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Menús'
        context['menu']   = 'menu'

        menus = self.get_queryset()
        categorias_con_menus = set(
            menus.values_list('categoria_menu', flat=True).distinct()
        ) if menus is not None else set()

        field = Menu._meta.get_field('categoria_menu')
        choices = field.choices if field.choices is not None else []

        context['categorias'] = [
            {'value': choice[0], 'display': choice[1]}
            for choice in choices
            if choice[0] in categorias_con_menus
        ]
        return context


class MenuCreateView(RolRequeridoMixin, CreateView):
    """Solo administradores pueden CREAR menús."""
    roles_permitidos = SOLO_ADMIN
    model = Menu
    template_name = 'forms/forms_menu_crear.html'
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Menú'
        context['title']  = 'Crear Nuevo Menú'
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
                if not formset.is_valid():
                    messages.error(self.request, 'Hay errores en los productos seleccionados.')
                    return self.form_invalid(form)

                productos_validos = [
                    f for f in formset.cleaned_data
                    if f and not f.get('DELETE', False)
                ]

                if not productos_validos:
                    messages.error(self.request, 'Debe agregar al menos un producto al menú.')
                    return self.form_invalid(form)

                self.object = form.save()
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


class MenuUpdateView(RolRequeridoMixin, UpdateView):
    """Solo administradores pueden EDITAR menús."""
    roles_permitidos = SOLO_ADMIN
    model = Menu
    template_name = 'forms/forms_menu_crear.html'
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Menú'
        context['title']  = 'Actualizar Menú'
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

                messages.success(self.request, f'Menú "{self.object.nombre}" actualizado exitosamente.')
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f'Error al actualizar: {str(e)}')
            return self.form_invalid(form)


class MenuDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden ELIMINAR menús."""
    roles_permitidos = SOLO_ADMIN
    model = Menu
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:menu:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Menú'
        return context

    def delete(self, request, *args, **kwargs):
        menu   = self.get_object()
        nombre = menu.nombre

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            menu.delete()
            return JsonResponse({'success': True, 'nombre': nombre})

        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Menú "{nombre}" eliminado exitosamente.')
        return response


@require_POST
@rol_requerido(*SOLO_ADMIN)
def menu_delete_ajax(request, pk):
    """Vista AJAX para eliminar menú — solo administradores."""
    try:
        menu   = get_object_or_404(Menu, pk=pk)
        nombre = menu.nombre
        menu.delete()
        return JsonResponse({'success': True, 'nombre': nombre})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


class MenuDetailView(RolRequeridoMixin, DetailView):
    """Todos los roles pueden VER el detalle de un menú."""
    roles_permitidos = TODOS
    model = Menu
    template_name = 'forms/menu_detalle.html'
    context_object_name = 'menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']   = f'Detalle: {self.object.nombre}'
        context['productos'] = self.object.menu_productos.select_related('producto').all()
        return context


# ══════════════════════════════════════════════
# VISTAS DE PEDIDOS
# Todos los roles tienen acceso a pedidos
# ══════════════════════════════════════════════

class PedidoListView(RolRequeridoMixin, ListView):
    """Todos los roles pueden ver pedidos."""
    roles_permitidos = TODOS
    model = Pedido
    template_name = 'forms/pedido_lista.html'
    context_object_name = 'pedidos'
    paginate_by = 12
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        queryset = Pedido.objects.prefetch_related('items__menu').all()
        estado = self.request.GET.get('estado')
        if estado and estado in dict(Pedido.ESTADO_CHOICES):
            queryset = queryset.filter(estado=estado)
        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']        = 'Gestión de Pedidos'
        context['menu']          = 'pedido'
        context['estados']       = Pedido.ESTADO_CHOICES
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['stats'] = {
            'total':     Pedido.objects.count(),
            'pendiente': Pedido.objects.filter(estado='pendiente').count(),
            'preparando': Pedido.objects.filter(estado='preparando').count(),
            'listo':     Pedido.objects.filter(estado='listo').count(),
            'entregado': Pedido.objects.filter(estado='entregado').count(),
            'cancelado': Pedido.objects.filter(estado='cancelado').count(),
        }
        return context


class PedidoCreateView(RolRequeridoMixin, View):
    """Todos los roles pueden CREAR pedidos."""
    roles_permitidos = TODOS
    template_name = 'forms/pedido_crear.html'

    def get(self, request, *args, **kwargs):
        return self._renderizar_pagina(request)

    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')

        if accion == 'agregar':
            menu_id = request.POST.get('menu_id')
            if not menu_id or not menu_id.isdigit():
                messages.error(request, 'Menú no válido.')
                return redirect('apl:menu:pedido_create')

            cantidad      = int(request.POST.get('cantidad', 1))
            observaciones = request.POST.get('observaciones', '').strip()
            carrito       = request.session.get('carrito', {})
            pedido_id     = request.session.get('pedido_editando')

            if pedido_id:
                pedido = get_object_or_404(Pedido, id=pedido_id)
                if pedido.estado in ['entregado', 'cancelado']:
                    messages.error(request, 'Este pedido ya fue entregado y no puede modificarse.')
                    return redirect('apl:menu:pedido_detail', pk=pedido.id)

            if menu_id in carrito:
                carrito[menu_id]['cantidad'] += cantidad
            else:
                carrito[menu_id] = {'tipo': 'menu', 'cantidad': cantidad, 'observaciones': observaciones}

            request.session['carrito'] = carrito
            request.session.modified   = True
            messages.success(request, 'Producto agregado al carrito')
            return redirect('apl:menu:pedido_create')

        elif accion == 'agregar_temporal':
            nombre   = request.POST.get('nombre')
            precio   = request.POST.get('precio')
            cantidad = int(request.POST.get('cantidad', 1))

            if not nombre or not precio:
                messages.error(request, 'Datos del producto temporal inválidos.')
                return redirect('apl:menu:pedido_create')

            carrito = request.session.get('carrito', {})
            temp_id = f"temp_{len(carrito) + 1}"
            carrito[temp_id] = {
                'tipo': 'temporal',
                'nombre': nombre,
                'precio': precio,
                'cantidad': cantidad
            }
            request.session['carrito'] = carrito
            request.session.modified   = True
            messages.success(request, 'Producto temporal agregado al carrito')
            return redirect('apl:menu:pedido_create')

        elif accion == 'actualizar':
            menu_id = request.POST.get('menu_id')
            if menu_id and menu_id.isdigit():
                cantidad = max(int(request.POST.get('cantidad', 1)), 1)
                carrito  = request.session.get('carrito', {})
                if menu_id in carrito:
                    carrito[menu_id]['cantidad'] = cantidad
                    request.session['carrito']   = carrito
                    request.session.modified     = True
            return redirect('apl:menu:pedido_create')

        elif accion == 'eliminar':
            key     = request.POST.get('key')
            carrito = request.session.get('carrito', {})
            if key in carrito:
                del carrito[key]
                request.session['carrito'] = carrito
                request.session.modified   = True
            return redirect("apl:menu:pedido_create")

        elif accion == 'confirmar':
            form    = PedidoForm(request.POST)
            carrito = request.session.get('carrito', {})

            if not carrito:
                messages.error(request, 'El carrito está vacío.')
                return self._renderizar_pagina(request, form=form)

            if not form.is_valid():
                messages.error(request, 'Corrige los errores del formulario.')
                return self._renderizar_pagina(request, form=form)

            pedido_id = request.session.get('pedido_editando')

            try:
                with transaction.atomic():
                    if pedido_id:
                        pedido = get_object_or_404(Pedido, id=pedido_id)
                        pedido.items.all().delete()
                        pedido.cliente_nombre = form.cleaned_data['cliente_nombre']
                        pedido.mesa_numero    = form.cleaned_data['mesa']
                        pedido.observaciones  = form.cleaned_data['observaciones']
                    else:
                        pedido = form.save(commit=False)

                    pedido.estado = 'pendiente'
                    pedido.save()

                    if not pedido_id:
                        crear_venta_desde_pedido(pedido)

                    for key, datos in carrito.items():
                        if not key.isdigit():
                            continue
                        menu = get_object_or_404(Menu, id=int(key))
                        PedidoItem.objects.create(
                            pedido=pedido,
                            menu=menu,
                            cantidad=datos['cantidad'],
                            precio_unitario=menu.get_precio_final(),
                            descuento_aplicado=menu.descuento or 0,
                            observaciones=datos.get('observaciones', '')
                        )

                    pedido.calcular_totales()
                    actualizar_venta_desde_pedido(pedido)

                    request.session.pop('carrito', None)
                    request.session.pop('pedido_editando', None)

                    messages.success(request, f'Pedido #{pedido.numero_pedido} actualizado correctamente')

                    origen = request.session.pop('origen_edicion', None)
                    if origen == 'venta' and hasattr(pedido, 'venta'):
                        return redirect('apl:venta:venta_detail', pk=pedido.venta.pk)

                    return redirect('apl:menu:pedido_detail', pk=pedido.pk)

            except Exception as e:
                messages.error(request, f'Error al guardar pedido: {e}')
                return self._renderizar_pagina(request, form=form)

    def _renderizar_pagina(self, request, form=None):
        carrito = request.session.get('carrito', {})

        menus_por_categoria = {}
        for menu in Menu.objects.filter(disponible=True).prefetch_related('menu_productos__producto'):
            categoria = menu.categoria_menu.nombre if menu.categoria_menu else "Sin categoría"
            menus_por_categoria.setdefault(categoria, []).append(menu)

        items_carrito   = []
        subtotal        = Decimal('0.00')
        descuento_total = Decimal('0.00')

        for key, datos in carrito.items():
            tipo = datos.get('tipo')

            if tipo == 'menu':
                try:
                    menu = Menu.objects.get(id=int(key), disponible=True)
                except (Menu.DoesNotExist, ValueError):
                    continue

                cantidad       = datos.get('cantidad', 1)
                precio_final   = menu.get_precio_final()
                subtotal_item  = precio_final * cantidad

                items_carrito.append({
                    'key': key,
                    'tipo': 'menu',
                    'menu': menu,
                    'cantidad': cantidad,
                    'precio_unitario': precio_final,
                    'subtotal': subtotal_item,
                    'observaciones': datos.get('observaciones', '')
                })

                subtotal += subtotal_item
                if menu.descuento > 0:
                    descuento_total += (menu.precio_base * cantidad) - subtotal_item

            elif tipo == 'temporal':
                cantidad      = datos.get('cantidad', 1)
                precio        = Decimal(str(datos.get('precio')))
                subtotal_item = precio * cantidad

                items_carrito.append({
                    'key': key,
                    'tipo': 'temporal',
                    'nombre': datos.get('nombre'),
                    'cantidad': cantidad,
                    'precio_unitario': precio,
                    'subtotal': subtotal_item
                })
                subtotal += subtotal_item

        pedido_id = request.session.get('pedido_editando')

        if form:
            form_pedido = form
        elif pedido_id:
            pedido      = get_object_or_404(Pedido, id=pedido_id)
            form_pedido = PedidoForm(instance=pedido)
        else:
            form_pedido = PedidoForm()

        context = {
            'titulo': 'Crear Nuevo Pedido',
            'menus_por_categoria': menus_por_categoria,
            'items_carrito': items_carrito,
            'subtotal': subtotal,
            'descuento_total': descuento_total,
            'total': subtotal,
            'form': form_pedido,
            'editando': bool(pedido_id),
        }
        return render(request, self.template_name, context)


class PedidoDetailView(RolRequeridoMixin, DetailView):
    """Todos los roles pueden ver el detalle de un pedido."""
    roles_permitidos = TODOS
    model = Pedido
    template_name = 'forms/pedido_detalle.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Pedido #{self.object.numero_pedido}'
        context['items']  = self.object.items.select_related('menu').all()
        context['form_estado'] = ActualizarEstadoPedidoForm(instance=self.object)
        return context


class PedidoUpdateEstadoView(RolRequeridoMixin, View):
    """
    Actualizar estado del pedido:
    - Todos pueden actualizar (mesero entrega, cocinero marca como listo, etc.)
    """
    roles_permitidos = TODOS

    def post(self, request, pk):
        pedido         = get_object_or_404(Pedido, pk=pk)
        estado_anterior = pedido.estado

        form = ActualizarEstadoPedidoForm(request.POST, instance=pedido)

        if not form.is_valid():
            messages.error(request, 'Error al actualizar el estado')
            return redirect('apl:menu:pedido_detail', pk=pk)

        pedido = form.save(commit=False)

        if estado_anterior == 'entregado':
            messages.warning(request, 'Este pedido ya fue entregado y no puede modificarse.')
            return redirect('apl:menu:pedido_detail', pk=pk)

        pedido.save()

        if pedido.estado == 'entregado' and estado_anterior != 'entregado':
            if hasattr(pedido, 'venta'):
                venta = pedido.venta
                venta.estado = 'pagado'
                venta.save()

            messages.success(
                request,
                f'Pedido #{pedido.numero_pedido} entregado y facturado correctamente.'
            )
        else:
            messages.success(
                request,
                f'Estado del pedido actualizado a: {pedido.get_estado_display()}'
            )

        return redirect('apl:menu:pedido_detail', pk=pk)


class PedidoDeleteView(RolRequeridoMixin, DeleteView):
    """Solo administradores pueden CANCELAR/ELIMINAR pedidos."""
    roles_permitidos = SOLO_ADMIN
    model = Pedido
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:menu:pedido_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cancelar Pedido'
        return context

    def delete(self, request, *args, **kwargs):
        pedido  = self.get_object()
        numero  = pedido.numero_pedido
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Pedido #{numero} cancelado exitosamente.')
        return response


class LimpiarCarritoView(RolRequeridoMixin, View):
    """Todos los roles pueden limpiar su carrito."""
    roles_permitidos = TODOS

    def post(self, request):
        request.session['carrito'] = {}
        request.session.modified   = True
        messages.info(request, 'Carrito limpiado')
        return redirect('apl:menu:pedido_create')


class PedidoUpdate(RolRequeridoMixin, View):
    """Todos los roles pueden editar pedidos (si no están entregados/cancelados)."""
    roles_permitidos = TODOS

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        origen = request.GET.get('from')

        if pedido.estado in ['entregado', 'cancelado']:
            messages.warning(
                request,
                f'El pedido #{pedido.numero_pedido} ya fue {pedido.get_estado_display()} y no puede editarse.'
            )
            if origen == 'venta' and hasattr(pedido, 'venta'):
                return redirect('apl:venta:venta_detail', pk=pedido.venta.pk)
            return redirect('apl:menu:pedido_detail', pk=pedido.pk)

        carrito = {}
        for item in pedido.items.all():
            key = str(item.menu_id)
            carrito[key] = {
                'tipo': 'menu',
                'cantidad': item.cantidad,
                'observaciones': item.observaciones or ''
            }

        request.session['carrito']        = carrito
        request.session['pedido_editando'] = pedido.id
        request.session['origen_edicion']  = origen
        request.session.modified           = True

        return redirect('apl:menu:pedido_create')