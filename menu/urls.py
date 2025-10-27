from menu.views import *
from django.urls import path

app_name = 'menu'

urlpatterns = [
    path('listar/', MenuListView.as_view(), name='menu_list'),
    path('crear/', MenuCreateView.as_view(), name='menu_create'),
    path('actualizar/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('eliminar/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),
]