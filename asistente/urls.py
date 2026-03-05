from django.urls import path
from . import views

app_name = 'asistente'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('enviar/', views.enviar_mensaje, name='enviar'),
    path('nueva/', views.nueva_conversacion, name='nueva'),
]