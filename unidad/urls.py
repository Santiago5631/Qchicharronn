from unidad import views
from django.urls import path

app_name = 'unidad'

urlpatterns = [
    path('listar/', views.UnidadListView.as_view(), name='unidad_list'),
    path('crear/', views.UnidadCreateView.as_view(), name='unidad_create'),
    path('editar/<int:pk>/', views.UnidadUpdateView.as_view(), name='unidad_edit'),
    path('eliminar/<int:pk>/', views.UnidadDeleteView.as_view(), name='unidad_delete'),
]