from django import forms
from django_select2.forms import Select2Widget
from categoria.models import Categoria
from marca.models import Marca
from proveedor.models import Proveedor
from unidad.models import Unidad
from .models import Producto


# --- Formulario principal de Producto ---
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'categoria', 'proveedor', 'tipo_uso', 'unidad', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': Select2Widget(attrs={'class': 'select2'}),
            'categoria': Select2Widget(attrs={'class': 'select2'}),
            'proveedor': Select2Widget(attrs={'class': 'select2'}),
            'tipo_uso': forms.Select(attrs={'class': 'form-control'}),
            'unidad': Select2Widget(attrs={'class': 'select2'}), 
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'required': True,
            }),
        }

    def clean_stock(self):
        """Valida que el stock no sea negativo."""
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock

    def __init__(self, *args, **kwargs):
        """Carga dinámica de opciones en los selects y etiquetas amigables."""
        super().__init__(*args, **kwargs)
        self.fields['marca'].queryset = Marca.objects.all()
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['proveedor'].queryset = Proveedor.objects.all()
        self.fields['unidad'].queryset = Unidad.objects.all()

        # Etiquetas y placeholders
        self.fields['marca'].empty_label = "Seleccione una marca"
        self.fields['categoria'].empty_label = "Seleccione una categoría"
        self.fields['proveedor'].empty_label = "Seleccione un proveedor"
        self.fields['unidad'].empty_label = "Seleccione una unidad"


# --- Formularios para los modales (solo los que se mantienen) ---
class MarcaModalForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class CategoriaModalForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class ProveedorModalForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nit']

class UnidadModalForm(forms.ModelForm):
    class Meta:
        modal = Unidad
        fields = ['nombre', 'descripcion']