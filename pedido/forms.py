from django import forms
from django.forms import inlineformset_factory, ModelForm
from .models import (
    Pedido, PedidoDetalle,
)

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa', 'estado']

PedidoDetalleFormSet = inlineformset_factory(
    Pedido,
    PedidoDetalle,
    fields=['menu', 'cantidad'],
    extra=1,
)
