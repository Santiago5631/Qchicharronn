import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


def verify_recaptcha(response_token, remoteip=None):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': response_token,
    }
    if remoteip:
        data['remoteip'] = remoteip
    try:
        r = requests.post(url, data=data, timeout=5)
        return r.json()
    except requests.RequestException:
        return {'success': False, 'error-codes': ['network-error']}


class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirige a la lista de usuarios
        return reverse_lazy('apl:dashboard')

    def form_valid(self, form):
        # Si estamos en modo desarrollo, permitimos omitir el reCAPTCHA
        if settings.DEBUG:
            messages.success(self.request, '¡Bienvenido! (reCAPTCHA omitido en desarrollo)')
            return super().form_valid(form)

        # Verificar reCAPTCHA antes de autenticar (Solo en producción o DEBUG=False)
        recaptcha_token = self.request.POST.get('g-recaptcha-response')

        if not recaptcha_token:
            messages.error(self.request, 'Por favor, completa el reCAPTCHA.')
            return self.form_invalid(form)

        # Verificar en el servidor de Google
        result = verify_recaptcha(recaptcha_token, self.request.META.get('REMOTE_ADDR'))

        if not result.get('success'):
            error_codes = result.get('error-codes', [])
            messages.error(self.request, f'reCAPTCHA inválido. Intenta de nuevo. Códigos: {error_codes}')
            return self.form_invalid(form)

        # Si todo está bien, continuar con el login normal
        messages.success(self.request, '¡Bienvenido!')
        return super().form_valid(form)


def custom_logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login:login')