from django import forms
from django.forms import inlineformset_factory
from .models import (
    Pedido,
    PedidoPlato,
    PedidoMenu,
)

# Formulario principal del pedido
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'empleado', 'estado', 'observacion']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# Formularios para los detalles de pedido
class PedidoPlatoForm(forms.ModelForm):
    class Meta:
        model = PedidoPlato
        fields = ['plato', 'cantidad']
        widgets = {
            'plato': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

PedidoPlatoFormSet = inlineformset_factory(
    Pedido, PedidoPlato,
    form=PedidoPlatoForm,
    extra=1,
    can_delete=True
)

class PedidoMenuForm(forms.ModelForm):
    class Meta:
        model = PedidoMenu
        fields = ['menu', 'cantidad']
        widgets = {
            'menu': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

PedidoMenuFormSet = inlineformset_factory(
    Pedido, PedidoMenu,
    form=PedidoMenuForm,
    extra=1,
    can_delete=True
)
