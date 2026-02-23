from django.urls import path
from . import views

app_name = 'backups'

urlpatterns = [
    path('gestion/', views.realizar_copia_seguridad, name='generar_backup'),
    path('google/auth/', views.google_auth, name='google_auth'),
    path('google/callback/', views.google_callback, name='google_callback'),
]