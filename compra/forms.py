from django import forms
from .models import *
from django.forms import ModelForm, inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.exceptions import ValidationError
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'producto', 'cantidad', 'fecha', 'precio', 'unidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'min': '0',
                'required': True,
            }),
            'precio': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',  # para valores con decimales
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
