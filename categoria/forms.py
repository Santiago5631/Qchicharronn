from django import forms
from .models import Categoria

# Formulario principal para crear/editar categorías
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
        }

    # forms.py → solo cambia esta línea en clean_nombre()
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or not nombre.strip():
            raise forms.ValidationError("El nombre de la categoría es obligatorio.")

        nombre = nombre.strip().title()

        # Excluimos el objeto actual al editar
        queryset = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(f"La categoría '{nombre}' ya existe.")

        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion or len(descripcion.strip()) < 5:
            raise forms.ValidationError("La descripción debe tener al menos 5 caracteres.")
        return descripcion.strip()
