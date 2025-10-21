from django.urls import path,include
import categoria
from mesa.views import *
from menu.views import *
from categoria.views import *
from marca.views import *
from proyecto_principal import views

app_name = 'proyecto_principal'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
