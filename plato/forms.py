from django import forms
from django.forms import inlineformset_factory
from django_select2.forms import Select2Widget
from .models import Plato, PlatoProducto
from unidad.models import Unidad  # 👈 importa Unidad

# Formulario principal de Plato
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio']


# Formulario intermedio para productos dentro de un plato
class PlatoProductoForm(forms.ModelForm):
    unidad = forms.ModelChoiceField(
        queryset=Unidad.objects.all(),  # 👈 carga todas las unidades automáticamente
        widget=Select2Widget(attrs={'class': 'select2'}),
        label='Unidad'
    )

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
