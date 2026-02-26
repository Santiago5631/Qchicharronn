# usuario/forms.py
from allauth.account.forms import ResetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

User = get_user_model()


# ══════════════════════════════════════════════
# FORMULARIO DE RESET DE CONTRASEÑA (ya existía)
# ══════════════════════════════════════════════
class CustomPasswordResetForm(ResetPasswordForm):
    def clean_email(self):
        email = super().clean_email()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo no está registrado en el sistema."
            )
        return email


# ══════════════════════════════════════════════
# FORMULARIO DE EDICIÓN DE PERFIL PROPIO
# Cada usuario puede editar sus propios datos
# ══════════════════════════════════════════════
class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nombre', 'cedula', 'email', 'numero_celular', 'foto_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cédula'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'numero_celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número celular'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'nombre': 'Nombre completo',
            'cedula': 'Cédula',
            'email': 'Correo electrónico',
            'numero_celular': 'Número celular',
            'foto_perfil': 'Foto de perfil',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar que el email no esté en uso por otro usuario
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este correo ya está registrado por otro usuario.")
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula:
            qs = User.objects.filter(cedula=cedula).exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Esta cédula ya está registrada por otro usuario.")
        return cedula


# ══════════════════════════════════════════════
# FORMULARIO DE CAMBIO DE CONTRASEÑA PROPIO
# ══════════════════════════════════════════════
class CambiarPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña actual'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        })
        self.fields['old_password'].label      = 'Contraseña actual'
        self.fields['new_password1'].label     = 'Nueva contraseña'
        self.fields['new_password2'].label     = 'Confirmar nueva contraseña'