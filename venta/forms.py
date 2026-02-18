from django import forms
from .models import Venta
from clientes.models import Cliente

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = [
            'cliente',
            'cliente_factura',
            'metodo_pago',
            'tipo_pedido',
            'mesa'
        ]

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label="Cliente Pedido"
    )

    cliente_factura = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label="Cliente Facturación"
    )
