from django.shortcuts import render, redirect
from plato.models import *
from django.views.generic import *
from plato.forms import PlatoForm, PlatoProductoFormSet
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.http import require_POST
from producto.models import Producto
from unidad.models import Unidad
import json


# 🔹 Mixin genérico para manejar mensajes de éxito
class SuccessMessageMixinCustom:
    success_message = None

    def form_valid(self, form, formset=None):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


# 🔹 Listar con función
def listar_plato(request):
    data = {
        "platos": "platos",
        "titulo": "Listado de Platos",
        "plato": Plato.objects.all()
    }
    return render(request, 'modulos/plato.html', data)


# 🔹 Listar con clase
class PlatoListView(ListView):
    model = Plato
    template_name = 'modulos/plato.html'
    context_object_name = 'platos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Platos'
        return context


# 🔹 Crear Plato
class PlatoCreateView(SuccessMessageMixinCustom, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'forms/formulario_crear_plato.html'
    success_url = reverse_lazy('apl:listar_plato')
    success_message = "✅ El plato se ha creado correctamente "

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        return render(request, self.template_name, {
            'form': form,
            'titulo': 'Crear Plato',
            'entidad': 'Plato',
            'productos': Producto.objects.all(),
            'unidades': Unidad.objects.all(),
        })

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        productos_json = request.POST.get("productos_json", "[]")
        productos_data = json.loads(productos_json)

        if form.is_valid():
            plato = form.save()
            for p in productos_data:
                producto = Producto.objects.get(id=p["id"])
                unidad = Unidad.objects.get(nombre=p["unidad"])
                PlatoProducto.objects.create(
                    plato=plato,
                    producto=producto,
                    cantidad=p["cantidad"],
                    unidad=unidad
                )
            messages.success(request, self.success_message)
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'titulo': 'Crear Plato',
            'entidad': 'Plato',
            'productos': Producto.objects.all(),
            'unidades': Unidad.objects.all(),
        })


# 🔹 Actualizar Plato
class PlatoUpdateView(SuccessMessageMixinCustom, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'forms/formulario_actualizar_plato.html'
    success_url = reverse_lazy('apl:listar_plato')
    success_message = "El plato se ha actualizado correctamente ✅"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = PlatoProductoFormSet(instance=self.object)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Editar Plato',
            'entidad': 'Plato'
        })

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = PlatoProductoFormSet(self.request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            plato = form.save()
            formset.instance = plato
            formset.save()
            messages.success(request, self.success_message)  # 👈 mensaje automático
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'titulo': 'Editar Plato',
            'entidad': 'Plato'
        })


# 🔹 Eliminar Plato (AJAX + SweetAlert)
@method_decorator(csrf_exempt, name="dispatch")
class PlatoDeleteView(DeleteView):
    model = Plato
    success_url = reverse_lazy('apl:listar_plato')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status": "ok"})


@require_POST
@csrf_exempt
def agregar_producto_ajax(request):
    producto_id = request.POST.get("producto")
    cantidad = request.POST.get("cantidad")
    unidad_id = request.POST.get("unidad")

    try:
        producto = Producto.objects.get(id=producto_id)
        unidad = Unidad.objects.get(id=unidad_id)

        data = {
            "id": producto.id,
            "nombre": producto.nombre,
            "cantidad": cantidad,
            "unidad": unidad.nombre,
        }
        return JsonResponse({"status": "ok", "producto": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
