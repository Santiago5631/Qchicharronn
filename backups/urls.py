from django.urls import path
from . import views

app_name = 'backups'

urlpatterns = [
    path('', views.realizar_copia_seguridad, name='generar_backup'),
    path('restaurar/', views.restaurar_backup, name='restaurar_backup'),
    path('descargar/<int:backup_id>/', views.descargar_backup, name='descargar_backup'),
    path('google/auth/', views.google_auth, name='google_auth'),
    path('google/callback/', views.google_callback, name='google_callback'),
]