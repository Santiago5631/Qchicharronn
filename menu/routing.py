# menu/routing.py  — ARCHIVO NUEVO
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/vista/(?P<area>parrilla|cocina)/$', consumers.VistaCocinaConsumer.as_asgi()),
]