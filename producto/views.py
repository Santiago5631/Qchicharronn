from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from categoria.models import Categoria
from marca.models import Marca
from proveedor.models import Proveedor
from .models import *
from .forms import (
    ProductoForm,
    MarcaModalForm,
    CategoriaModalForm,
    ProveedorModalForm,

)
import json
from django.shortcuts import redirect
from django.contrib import messages


class successMessageMixin:
    success_message = None

    def form_valid(self, form, formset=None):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response()


# TUS VISTAS ORIGINALES - NO CAMBIAR
class ProductoListView(ListView):
    model = Producto
    template_name = 'modulos/producto.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de productos'
        context['modelo'] = 'producto'
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'forms/formulario_crear_producto.html'
    success_url = reverse_lazy('apl:producto:producto_list')
    success_message = "Producto creado exitosamente"

    def get_context_data(self, **kwargs):
        # Inicializar self.object si no existe
        if not hasattr(self, 'object'):
            self.object = None

        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Producto'

        # Agregar formularios para los modales
        context['marca_form'] = MarcaModalForm()
        context['categoria_form'] = CategoriaModalForm()
        context['proveedor_form'] = ProveedorModalForm()

        return context

    def post(self, request, *args, **kwargs):
        # IMPORTANTE: Inicializar self.object
        self.object = None

        # Detectar qué formulario se envió
        if 'crear_marca' in request.POST:
            return self.crear_marca(request)
        elif 'crear_categoria' in request.POST:
            return self.crear_categoria(request)
        elif 'crear_proveedor' in request.POST:
            return self.crear_proveedor(request)
        else:
            # Formulario principal de producto
            return super().post(request, *args, **kwargs)

    def crear_marca(self, request):
        form = MarcaModalForm(request.POST)
        if form.is_valid():
            marca = form.save()
            messages.success(request, f'Marca "{marca.nombre}" creada exitosamente')
            return redirect(request.path)
        else:
            messages.error(request, 'Error al crear la marca. Verifique los datos.')
            # Ya no es necesario pasar marca_form, get_context_data lo maneja
            return self.render_to_response(self.get_context_data())

    def crear_categoria(self, request):
        form = CategoriaModalForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente')
            return redirect(request.path)
        else:
            messages.error(request, 'Error al crear la categoría. Verifique los datos.')
            return self.render_to_response(self.get_context_data())

    def crear_proveedor(self, request):
        form = ProveedorModalForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" creado exitosamente')
            return redirect(request.path)
        else:
            messages.error(request, 'Error al crear el proveedor. Verifique los datos.')
            return self.render_to_response(self.get_context_data())


    def form_valid(self, form):
        messages.success(self.request, 'Producto creado exitosamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el producto. Verifique los datos.')
        return super().form_invalid(form)


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'forms/formulario_actualizacion.html'
    form_class = ProductoForm
    success_message = "Producto creado exitosamente"

    def get_success_url(self):
        return reverse_lazy('apl:producto:producto_list')


class ProductoDeleteView(DeleteView):
    model = Producto
    success_url = reverse_lazy('apl:producto:   producto_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


# NUEVAS VISTAS AJAX PARA CREAR FOREIGN KEYS
@require_POST
def crear_marca_ajax(request):
    """Vista AJAX para crear nueva marca"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        descripcion = data.get('descripcion', '').strip()
        pais_origen = data.get('pais_origen', '').strip()

        if not nombre:
            return JsonResponse({
                'success': False,
                'error': 'El nombre de la marca es requerido'
            })

        if not pais_origen:
            return JsonResponse({
                'success': False,
                'error': 'El país de origen es requerido'
            })

        # Verificar si ya existe
        if Marca.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe una marca con este nombre'
            })

        # Crear nueva marca
        marca = Marca.objects.create(
            nombre=nombre,
            descripcion=descripcion if descripcion else None,
            pais_origen=pais_origen
        )

        return JsonResponse({
            'success': True,
            'id': marca.id,
            'text': str(marca)  # Para Select2
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def crear_categoria_ajax(request):
    """Vista AJAX para crear nueva categoría"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        descripcion = data.get('descripcion', '').strip()

        if not nombre:
            return JsonResponse({
                'success': False,
                'error': 'El nombre de la categoría es requerido'
            })

        if Categoria.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe una categoría con este nombre'
            })

        categoria = Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion if descripcion else None
        )

        return JsonResponse({
            'success': True,
            'id': categoria.id,
            'text': str(categoria)
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def crear_proveedor_ajax(request):
    """Vista AJAX para crear nuevo proveedor"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        nit = data.get('nit', '').strip()

        if not nombre or not nit:
            return JsonResponse({
                'success': False,
                'error': 'El nombre y el NIT del proveedor son requeridos'
            })

        if Proveedor.objects.filter(nombre=nombre).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe un proveedor con este nombre'
            })

        if Proveedor.objects.filter(nit=nit).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ya existe un proveedor con este NIT'
            })

        proveedor = Proveedor.objects.create(
            nombre=nombre,
            nit=nit
        )

        return JsonResponse({
            'success': True,
            'id': proveedor.id,
            'text': str(proveedor)
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Datos JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
# Create your views here.
