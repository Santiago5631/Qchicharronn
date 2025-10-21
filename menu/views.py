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
    success_url = reverse_lazy('apl:menu_list')

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

                # Guardar el menú
                self.object = form.save(commit=False)

                # Configurar fecha si no existe
                if not self.object.fecha_creacion:
                    self.object.fecha_creacion = timezone.now()

                # Configurar content_type según el tipo
                if tipo_item == 'plato' and plato_id:
                    self.object.content_type = ContentType.objects.get_for_model(Plato)
                    self.object.object_id = plato_id.id
                else:
                    self.object.content_type = None
                    self.object.object_id = None

                # Guardar el objeto
                self.object.save()

                # Si es tipo 'productos', guardar el formset
                if tipo_item == 'productos':
                    if formset.is_valid():
                        formset.instance = self.object
                        formset.save()
                    else:
                        print("Errores en formset:", formset.errors)
                        raise ValueError("Error al guardar productos")

                messages.success(self.request, f'Menú "{self.object.nombre}" creado exitosamente.')
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f'Error al crear el menú: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        print("Errores del formulario:", form.errors)
        return super().form_invalid(form)


class MenuUpdateView(UpdateView):
    model = Menu
    template_name = 'forms/formulario_actualizacion.html'
    form_class = MenuForm
    success_url = reverse_lazy('apl:menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Menú'
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
                    if formset.is_valid():
                        formset.instance = self.object
                        formset.save()
                    else:
                        raise ValueError("Error al actualizar productos")

                messages.success(self.request, f'Menú "{self.object.nombre}" actualizado exitosamente.')
                return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f'Error al actualizar el menú: {str(e)}')
            return self.form_invalid(form)


class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'forms/confirmar_eliminacion.html'
    success_url = reverse_lazy('apl:menu_list')

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