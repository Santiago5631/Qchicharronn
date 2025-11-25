from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.InventarioDashboardView.as_view(), name='dashboard'),

    # Gestión de inventario diario
    path('apertura/', views.AperturaInventarioView.as_view(), name='apertura'),
    path('cierre/<int:pk>/', views.CierreInventarioView.as_view(), name='cierre'),
    path('detalle/<int:pk>/', views.InventarioDetalleView.as_view(), name='detalle'),
    path('lista/', views.InventarioListView.as_view(), name='lista'),

    # Ajustes y movimientos
    path('ajuste/', views.AjusteInventarioView.as_view(), name='ajuste'),

    # Reportes
    path('reporte/', views.ReporteInventarioView.as_view(), name='reporte'),
    path('historial/', views.HistorialStockView.as_view(), name='historial'),
]