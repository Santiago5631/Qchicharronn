# usuario/forms.py
from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    """
    Formulario de registro que elimina cualquier referencia a 'username'
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Forzamos la eliminación de username (aunque ya no exista en el modelo)
        self.fields.pop('username', None)

    def signup(self, request, user):
        # Guardamos campos adicionales si los tienes en el formulario
        # (puedes agregar más si quieres: cedula, cargo, etc.)
        user.nombre = self.cleaned_data.get('nombre', '')
        user.cedula = self.cleaned_data.get('cedula', '')
        user.cargo = self.cleaned_data.get('cargo', 'operador')
        user.numero_celular = self.cleaned_data.get('numero_celular', '')
        user.estado = self.cleaned_data.get('estado', 'activo')
        user.save()