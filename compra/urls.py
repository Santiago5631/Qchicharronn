from compra.views import *
from django.urls import path

app_name = 'compra'
urlpatterns = [

    # -------------------- Compra --------------------
    path('listar/', CompraListView.as_view(), name='compra_list'),
    path('crear/', CompraCreateView.as_view(), name='crear_compra'),
    path('editar/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),
    path('eliminar/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),
    path('exportar/excel/', exportar_compras_excel, name='exportar_excel'),
    path('exportar/pdf/', exportar_compras_pdf, name='exportar_pdf'),
    path('factura/<int:pk>/', generar_factura_pdf, name='generar_factura_pdf'),
]
