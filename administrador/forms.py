from django import forms
from .models import *
from django.forms import ModelForm, inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.exceptions import ValidationError
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = ['usuario', 'nivel_prioridad']
        widgets = {
            'nivel_prioridad': forms.NumberInput(attrs={
                'min': '0',
                'required': True,
            }),
        }

    # Validación a nivel de Django (backend)
    def clean_nivel_prioridad(self):
        nivel_prioridad = self.cleaned_data.get('nivel_prioridad')
        print(f"DEBUG: nivel_prioridad = {nivel_prioridad}, tipo: {type(nivel_prioridad)}")  # Para debug

        if nivel_prioridad is not None and nivel_prioridad < 0:
            raise forms.ValidationError("El nivel de prioridad no puede ser negativo.")
        return nivel_prioridad

    def clean(self):
        cleaned_data = super().clean()
        nivel_prioridad = cleaned_data.get('nivel_prioridad')

        # Validación adicional en clean general
        if nivel_prioridad is not None and nivel_prioridad < 0:
            raise forms.ValidationError("El nivel de prioridad no puede ser negativo.")

        return cleaned_data