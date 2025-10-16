from django import forms
from django.forms import inlineformset_factory
from django_select2.forms import Select2Widget
from .models import Plato
from producto.models import Producto

# Formulario principal de Plato
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'marca', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'categoria': forms.Select(attrs={'class': 'form-control select2'}),
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
        }

# Si cada plato tiene ingredientes (productos primarios)
class PlatoProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre']

PlatoProductoFormSet = inlineformset_factory(
    Plato, Producto,
    form=PlatoProductoForm,
    extra=1,
    can_delete=True
)
