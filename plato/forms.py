from django import forms
from django.forms import inlineformset_factory
from django_select2.forms import Select2Widget
from .models import Plato, PlatoProducto

# Formulario principal de Plato
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio']

class PlatoProductoForm(forms.ModelForm):
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad', 'unidad']
        widgets = {
            'producto': Select2Widget(attrs={'class': 'select2'}),
        }

PlatoProductoFormSet = inlineformset_factory(
    Plato,
    PlatoProducto,
    form=PlatoProductoForm,
    extra=1,
    can_delete=True
)
