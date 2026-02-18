from django.urls import path
from .views import ClienteListView, ClienteCreateView

app_name = "clientes"

urlpatterns = [
    path("", ClienteListView.as_view(), name="lista_clientes"),
    path("crear/", ClienteCreateView.as_view(), name="crear_cliente"),
]
