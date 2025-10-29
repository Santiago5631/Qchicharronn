from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import transaction
from django.contrib import messages
from .forms import *
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Menu, MenuProducto


class MenuListView(ListView):
    model = Menu
    template_name = 'modulos/menu.html'
    context_object_name = 'menus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Menús'
        context['menu'] = 'menu'
        return context


class MenuCreateView(CreateView):
    model = Menu
    template_name = 'forms/forms_menu_crear.html'
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu:menu_list')  # ✅ CORREGIDO

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo Menú'
        context['title'] = 'Crear nuevo Menú'
        context['modulo'] = "menu"
        context['productos'] = Producto.objects.all()
        context['platos'] = Plato.objects.all()

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
                # Obtener datos del formulario
                tipo_item = form.cleaned_data.get('tipo_item')
                plato_id = form.cleaned_data.get('plato_id')

                print(f"DEBUG - Tipo item: {tipo_item}")  # Debug
                print(f"DEBUG - Plato ID: {plato_id}")  # Debug

                # ✅ VALIDACIÓN: Verificar que se seleccionó un tipo
                if not tipo_item:
                    messages.error(self.request, 'Debe seleccionar un tipo de ítem.')
                    return self.form_invalid(form)

                # ✅ VALIDACIÓN: Si es tipo plato, debe seleccionar un plato
                if tipo_item == 'plato' and not plato_id:
                    messages.error(self.request, 'Debe seleccionar un plato cuando el tipo es "Plato Compuesto".')
                    return self.form_invalid(form)

                # ✅ VALIDACIÓN: Si es tipo productos, debe haber al menos un producto
                if tipo_item == 'productos':
                    if not formset.is_valid():
                        print("DEBUG - Errores en formset:", formset.errors)  # Debug
                        messages.error(self.request, 'Hay errores en los productos seleccionados.')
                        return self.form_invalid(form)

                    # Verificar que hay al menos un producto válido
                    productos_validos = [f for f in formset.cleaned_data if f and not f.get('DELETE', False)]
                    if not productos_validos:
                        messages.error(self.request,
                                       'Debe agregar al menos un producto cuando el tipo es "Productos Individuales".')
                        return self.form_invalid(form)

                # Guardar el menú
                self.object = form.save(commit=False)

                # Configurar fecha si no existe
                if not self.object.fecha_creacion:
                    self.object.fecha_creacion = timezone.now()

                # Configurar content_type según el tipo
                if tipo_item == 'plato' and plato_id:
                    self.object.content_type = ContentType.objects.get_for_model(Plato)
                    self.object.object_id = plato_id.id
                    print(f"DEBUG - Guardando como plato: {plato_id.nombre}")  # Debug
                else:
                    self.object.content_type = None
                    self.object.object_id = None
                    print("DEBUG - Guardando como menú simple o productos")  # Debug

                # Guardar el objeto
                self.object.save()
                print(f"DEBUG - Menú guardado con ID: {self.object.id}")  # Debug

                # Si es tipo 'productos', guardar el formset
                if tipo_item == 'productos':
                    formset.instance = self.object
                    formset.save()
                    print(f"DEBUG - Productos guardados: {self.object.menu_productos.count()}")  # Debug

                messages.success(self.request, f'Menú "{self.object.nombre}" creado exitosamente.')
                return redirect(self.success_url)

        except Exception as e:
            print(f"DEBUG - Error al guardar: {str(e)}")  # Debug
            import traceback
            traceback.print_exc()  # Imprime el stack trace completo
            messages.error(self.request, f'Error al crear el menú: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        print("DEBUG - Errores del formulario:", form.errors)  # Debug
        context = self.get_context_data()
        print("DEBUG - Errores del formset:", context['formset'].errors)  # Debug
        return super().form_invalid(form)


class MenuUpdateView(UpdateView):
    model = Menu
    template_name = 'forms/forms_menu_crear.html'  # ✅ Mismo template que crear
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu:menu_list')  # ✅ CORREGIDO

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Menú'
        context['title'] = 'Actualizar Menú'  # ✅ Agregado
        context['modulo'] = "menu"
        context['productos'] = Producto.objects.all()
        context['platos'] = Plato.objects.all()

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
                tipo_item = form.cleaned_data.get('tipo_item')
                plato_id = form.cleaned_data.get('plato_id')

                print(f"DEBUG - Actualizando - Tipo item: {tipo_item}")  # Debug

                # ✅ VALIDACIONES
                if not tipo_item:
                    messages.error(self.request, 'Debe seleccionar un tipo de ítem.')
                    return self.form_invalid(form)

                if tipo_item == 'plato' and not plato_id:
                    messages.error(self.request, 'Debe seleccionar un plato.')
                    return self.form_invalid(form)

                if tipo_item == 'productos':
                    if not formset.is_valid():
                        messages.error(self.request, 'Hay errores en los productos.')
                        return self.form_invalid(form)

                    productos_validos = [f for f in formset.cleaned_data if f and not f.get('DELETE', False)]
                    if not productos_validos:
                        messages.error(self.request, 'Debe tener al menos un producto.')
                        return self.form_invalid(form)

                self.object = form.save(commit=False)

                # Actualizar content_type
                if tipo_item == 'plato' and plato_id:
                    self.object.content_type = ContentType.objects.get_for_model(Plato)
                    self.object.object_id = plato_id.id
                else:
                    self.object.content_type = None
                    self.object.object_id = None

                self.object.save()

                # Actualizar productos si es tipo 'productos'
                if tipo_item == 'productos':
                    formset.instance = self.object
                    formset.save()
                else:
                    # Si cambió de productos a otro tipo, eliminar productos existentes
                    self.object.menu_productos.all().delete()

                messages.success(self.request, f'Menú "{self.object.nombre}" actualizado exitosamente.')
                return redirect(self.success_url)

        except Exception as e:
            print(f"DEBUG - Error al actualizar: {str(e)}")  # Debug
            import traceback
            traceback.print_exc()
            messages.error(self.request, f'Error al actualizar el menú: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        print("DEBUG - Errores del formulario:", form.errors)  # Debug
        return super().form_invalid(form)


class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:menu:menu_list')  # ✅ CORREGIDO

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Menú'
        return context

    def delete(self, request, *args, **kwargs):
        menu = self.get_object()
        nombre = menu.nombre
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Menú "{nombre}" eliminado exitosamente.')
        return response