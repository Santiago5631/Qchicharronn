from allauth.account.forms import ResetPasswordForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomPasswordResetForm(ResetPasswordForm):

    def clean_email(self):
        email = super().clean_email()

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo no está registrado en el sistema."
            )

        return email
