from django import forms
from django.forms import inlineformset_factory, ModelForm
from .models import (
    Pedido, PedidoDetalle,
)
from mesa.models import Mesa

class PedidoForm(ModelForm):
    mesa = forms.ModelChoiceField(
        queryset=Mesa.objects.all(),
        label="Mesa",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Pedido
        fields = ['mesa', 'estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

PedidoDetalleFormSet = inlineformset_factory(
    Pedido,
    PedidoDetalle,
    fields=['menu', 'cantidad'],
    extra=1,
)