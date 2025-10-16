from django import forms
from .models import *
from django.forms import ModelForm, inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.exceptions import ValidationError
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['pedido', 'total', 'metodo_pago', 'estado', 'admin']
        widgets = {
            'total': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',  # para valores con decimales
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is not None and total < 0:
            raise forms.ValidationError("El total no puede ser negativo.")
        return total

    def clean(self):
        cleaned_data = super().clean()
        pedido = cleaned_data.get('pedido')

        if pedido is None:
            raise forms.ValidationError("Debes seleccionar un pedido.")

        # Validación: un pedido no puede tener más de una venta pagada
        if Venta.objects.filter(pedido=pedido, estado="pagado").exists():
            raise forms.ValidationError(
                f"El pedido {pedido.id} ya tiene una venta registrada como pagada."
            )

        return cleaned_data