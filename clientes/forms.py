from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        widgets = {
            "direccion": forms.Textarea(attrs={"rows": 2}),
        }
