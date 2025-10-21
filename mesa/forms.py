from django import forms
from .models import  *

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad', 'ubicacion']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: M-001'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 4',
                'min': '1'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Terraza'
            }),
        }
        labels = {
            'numero': 'Número de Mesa',
            'capacidad': 'Capacidad (personas)',
            'ubicacion': 'Ubicación',
        }

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if not numero:
            raise forms.ValidationError("El número de mesa es obligatorio.")
        if ' ' in numero:
            raise forms.ValidationError("El número de mesa no puede contener espacios.")
        instance = self.instance
        if Mesa.objects.filter(numero=numero).exclude(pk=instance.pk).exists():
            raise forms.ValidationError(f"Ya existe una mesa con el número '{numero}'.")
        return numero.upper()

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad is None:
            raise forms.ValidationError("La capacidad es obligatoria.")
        if capacidad < 1:
            raise forms.ValidationError("La capacidad debe ser al menos 1 persona.")
        if capacidad > 20:
            raise forms.ValidationError("La capacidad máxima es de 20 personas.")
        return capacidad

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion or not ubicacion.strip():
            raise forms.ValidationError("La ubicación es obligatoria.")
        if len(ubicacion.strip()) < 3:
            raise forms.ValidationError("La ubicación debe tener al menos 3 caracteres.")
        return ubicacion.strip().title()