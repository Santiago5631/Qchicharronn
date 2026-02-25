# usuario/permisos.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

# ── Constantes de roles ──
ADMINISTRADOR = 'administrador'
COCINERO      = 'cocinero'
PARRILLA      = 'parrilla'
MESERO        = 'mesero'

TODOS      = [ADMINISTRADOR, COCINERO, PARRILLA, MESERO]
COCINAS    = [ADMINISTRADOR, COCINERO, PARRILLA]
SOLO_ADMIN = [ADMINISTRADOR]
ADMIN_MESERO = [ADMINISTRADOR, MESERO]


# ══════════════════════════════════════════
# MIXIN para Vistas de Clase (CBV)
# ══════════════════════════════════════════
class RolRequeridoMixin(LoginRequiredMixin):
    """
    Protege vistas de clase según el campo 'cargo' del usuario.

    Uso:
        class MiVista(RolRequeridoMixin, ListView):
            roles_permitidos = ['administrador', 'cocinero']
    """
    roles_permitidos = []
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.cargo not in self.roles_permitidos:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# ══════════════════════════════════════════
# DECORADOR para Vistas de Función
# ══════════════════════════════════════════
def rol_requerido(*roles):
    """
    Protege vistas de función según el campo 'cargo' del usuario.

    Uso:
        @rol_requerido('administrador', 'mesero')
        def mi_vista(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.conf import settings
                from django.shortcuts import redirect
                return redirect(settings.LOGIN_URL)
            if request.user.cargo not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator