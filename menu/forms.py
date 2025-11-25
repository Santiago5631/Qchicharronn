from django import forms
from django.forms import inlineformset_factory
from .models import Menu, MenuProducto, Pedido, PedidoItem
from producto.models import Producto


class MenuForm(forms.ModelForm):
    """Formulario para crear/editar menús"""

    class Meta:
        model = Menu
        fields = [
            'nombre',
            'descripcion',
            'categoria_menu',
            'precio_base',
            'descuento',
            'disponible',
            'imagen',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Combo Especial del Día',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe el menú...',
                'rows': 4,
            }),
            'categoria_menu': forms.Select(attrs={
                'class': 'form-control',
            }),
            'precio_base': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00',
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        labels = {
            'nombre': 'Nombre del Menú',
            'descripcion': 'Descripción',
            'categoria_menu': 'Categoría',
            'precio_base': 'Precio Base',
            'descuento': 'Descuento (%)',
            'disponible': 'Disponible',
            'imagen': 'Imagen del Menú',
        }

    def clean_precio_base(self):
        precio = self.cleaned_data.get('precio_base')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento is None:
            return 0
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100%.")
        return descuento


class MenuProductoInlineForm(forms.ModelForm):
    """Formulario inline para agregar productos al menú"""

    class Meta:
        model = MenuProducto
        fields = ['producto', 'cantidad', 'orden']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control producto-select',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '1.00',
                'value': '1.00',
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0',
            }),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'orden': 'Orden',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar productos disponibles
        self.fields['producto'].queryset = Producto.objects.filter(
            disponible=True
        ).order_by('nombre')

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad


# Formset para productos del menú
MenuProductoFormSet = inlineformset_factory(
    Menu,
    MenuProducto,
    form=MenuProductoInlineForm,
    extra=3,  # 3 filas vacías por defecto
    can_delete=True,
    min_num=1,  # Al menos 1 producto requerido
    validate_min=True,
)

class PedidoForm(forms.ModelForm):
    """Formulario para crear pedidos - SOLO datos del cliente"""

    class Meta:
        model = Pedido
        fields = [
            'cliente_nombre',
            'mesa_numero',
            'observaciones',
            # ← ¡ELIMINADO 'estado' DE AQUÍ!
        ]
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente',
                'required': True,
                'autofocus': True,
            }),
            'mesa_numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de mesa (opcional)',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales (ej: para llevar, sin picante, etc.)',
                'rows': 3,
            }),
        }
        labels = {
            'cliente_nombre': 'Nombre del Cliente',
            'mesa_numero': 'Mesa N°',
            'observaciones': 'Observaciones',
        }

    def clean_cliente_nombre(self):
        nombre = self.cleaned_data.get('cliente_nombre')
        if not nombre:
            raise forms.ValidationError("El nombre del cliente es obligatorio.")
        nombre = nombre.strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

class AgregarAlPedidoForm(forms.Form):
    """Formulario simple para agregar un menú al pedido"""
    menu_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'value': '1',
        }),
        label='Cantidad'
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Observaciones (opcional)...',
            'rows': 2,
        }),
        label='Observaciones'
    )


class ActualizarEstadoPedidoForm(forms.ModelForm):
    """Formulario para actualizar solo el estado del pedido"""

    class Meta:
        model = Pedido
        fields = ['estado', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }
        labels = {
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }