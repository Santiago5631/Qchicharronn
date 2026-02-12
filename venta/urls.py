from venta.views import *
from django.urls import path

app_name = 'venta'
urlpatterns = [

    # -------------------- Venta --------------------
    path('listar/', VentaListView.as_view(), name='venta_list'),
    path('detalle/<int:pk>/', VentaDetailView.as_view(), name='venta_detail'),
    path('factura/<int:pk>/', VentaFacturaView.as_view(), name='factura'),
    path('finalizar/<int:pk>/', VentaFinalizarView.as_view(), name='venta_finalizar'),

    ]

