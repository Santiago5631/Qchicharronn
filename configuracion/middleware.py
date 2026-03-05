from django.shortcuts import redirect
from django.conf import settings


class RequireLoginMiddleware:
    EXEMPT_PREFIXES = [
        '/login/',
        '/accounts/',
        '/admin/',
        '/static/',
        '/media/',
        '/captcha/',
        '/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if request.user.is_authenticated:
            return self.get_response(request)

        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        next_param = f"?next={path}" if path != '/' else ''
        return redirect(settings.LOGIN_URL + next_param)