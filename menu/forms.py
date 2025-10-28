from django import forms
from django.forms import inlineformset_factory
from .models import Menu, MenuProducto
from plato.models import *
from producto.models import *

class MenuForm(forms.ModelForm):
    """Formulario principal para crear/editar menús"""
    TIPO_ITEM_CHOICES = [
        ('', '-- Seleccionar --'),
        ('productos', 'Productos Individuales (Múltiples)'),
        ('plato', 'Plato Compuesto'),
        ('menu_simple', 'Menú Simple'),
    ]

    tipo_item = forms.ChoiceField(
        choices=TIPO_ITEM_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo_item',
        }),
        label='Tipo de Ítem'
    )

    plato_id = forms.ModelChoiceField(
        queryset=Plato.objects.all(),
        required=False,  # Mantener como no requerido
        empty_label='-- Seleccionar Plato --',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_plato_id',
        }),
        label='Plato'
    )

    class Meta:
        model = Menu
        fields = [
            'nombre',
            'descripcion',
            'precio_menu',
            'descuento',
            'categoria_menu',
            'disponible',
            'fecha_creacion',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_nombre',
                'placeholder': 'Ej: Combo Especial',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_descripcion',
                'placeholder': 'Describe el ítem del menú...',
                'rows': 4,
            }),
            'precio_menu': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_precio_menu',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_descuento',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00',
                'value': '0',
            }),
            'categoria_menu': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_categoria_menu',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_disponible',
            }),
            'fecha_creacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'id_fecha_creacion',
                'type': 'datetime-local',
            }, format='%Y-%m-%dT%H:%M'),
        }
        labels = {
            'nombre': 'Nombre del Menú',
            'descripcion': 'Descripción',
            'precio_menu': 'Precio',
            'descuento': 'Descuento (%)',
            'categoria_menu': 'Categoría del Menú',
            'disponible': 'Disponible',
            'fecha_creacion': 'Fecha de Creación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Forzar campos requeridos
        self.fields['nombre'].required = True
        self.fields['descripcion'].required = True
        self.fields['precio_menu'].required = True
        self.fields['categoria_menu'].required = True
        self.fields['descuento'].required = True
        self.fields['disponible'].required = True
        self.fields['fecha_creacion'].required = False  # opcional

        self.fields['fecha_creacion'].input_formats = ['%Y-%m-%dT%H:%M']

        # Si estamos editando, determinar el tipo
        if self.instance and self.instance.pk:
            if self.instance.menu_productos.exists():
                self.fields['tipo_item'].initial = 'productos'
            elif self.instance.content_type:
                model_class = self.instance.content_type.model_class()
                if model_class == Plato:
                    self.fields['tipo_item'].initial = 'plato'
                    if self.instance.item:
                        self.fields['plato_id'].initial = self.instance.item.id
            else:
                self.fields['tipo_item'].initial = 'menu_simple'

    def clean_precio_menu(self):
        precio = self.cleaned_data.get('precio_menu')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento is None:
            return 0
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100%.")
        return descuento

    # MÉTODO clean() CORREGIDO - SIN VALIDACIÓN DE CAMPOS VACÍOS
    def clean(self):
        cleaned_data = super().clean()
        # Ya no validamos si los campos están vacíos
        # La validación se hace en la vista
        return cleaned_data


# Formulario inline para MenuProducto (sin cambios)

# Formulario inline para MenuProducto (sin cambios)
class MenuProductoInlineForm(forms.ModelForm):
    """Formulario inline para productos dentro de un menú"""

    class Meta:
        model = MenuProducto
        fields = ['producto', 'cantidad', 'orden']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '1.00'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad


# Formset para MenuProducto (sin cambios)
MenuProductoFormSet = inlineformset_factory(
    Menu,
    MenuProducto,
    form=MenuProductoInlineForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)

