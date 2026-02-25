from django.shortcuts import redirect
from django.conf import settings

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("[RequireLoginMiddleware] Inicializado correctamente")

    def __call__(self, request):
        path = request.path_info
        print(f"[RequireLoginMiddleware] Ejecutando para: {path} | Autenticado: {request.user.is_authenticated}")

        if request.user.is_authenticated:
            print("[RequireLoginMiddleware] Usuario autenticado → pasando")
            return self.get_response(request)

        # Rutas permitidas sin login
        exempt_prefixes = [
            '/login/',
            '/accounts/',
            '/admin/',
            '/static/',
            '/media/',
            '/captcha/',
            '/',                # home si es público
            # NO agregues '/apps/' aquí, porque eso dejaría TODAS las apps sin protección
        ]

        is_exempt = any(path.startswith(prefix) for prefix in exempt_prefixes)
        print(f"[RequireLoginMiddleware] ¿Es exenta? {is_exempt}")

        if is_exempt:
            print(f"[RequireLoginMiddleware] Ruta exenta → pasando")
            return self.get_response(request)

        # Redirigir si no autenticado y no exenta
        print(f"[RequireLoginMiddleware] REDIRIGIENDO a login desde: {path}")
        next_param = f"?next={path}" if path != '/' else ''
        return redirect(settings.LOGIN_URL + next_param)