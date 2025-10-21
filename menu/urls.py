from menu.views import *
from django.urls import path

app_name = 'menu'

urlpatterns = [
    path('menus/listar/', MenuListView.as_view(), name='menu_list'),
    path('menus/crear/', MenuCreateView.as_view(), name='menu_create'),
    path('menus/actualizar/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('menus/eliminar/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),
]