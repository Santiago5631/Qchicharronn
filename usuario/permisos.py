# usuario/permisos.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

# ── Constantes de roles ──
ADMINISTRADOR = 'administrador'
COCINERO      = 'cocinero'
PARRILLA      = 'parrilla'
MESERO        = 'mesero'
CAJERA        = 'cajera'          # ← ROL NUEVO

TODOS         = [ADMINISTRADOR, COCINERO, PARRILLA, MESERO, CAJERA]
COCINAS       = [ADMINISTRADOR, COCINERO, PARRILLA]
SOLO_ADMIN    = [ADMINISTRADOR]
ADMIN_MESERO  = [ADMINISTRADOR, MESERO]
ADMIN_CAJERA  = [ADMINISTRADOR, CAJERA]                    # ← NUEVO
CAJA          = [ADMINISTRADOR, MESERO, CAJERA]            # ← NUEVO (ventas/pedidos/mesas)


# ══════════════════════════════════════════════
# MIXIN para Vistas de Clase (CBV)
# ══════════════════════════════════════════════
class RolRequeridoMixin(LoginRequiredMixin):
    roles_permitidos = []
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.cargo not in self.roles_permitidos:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# ══════════════════════════════════════════════
# DECORADOR para Vistas de Función
# ══════════════════════════════════════════════
def rol_requerido(*roles):
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