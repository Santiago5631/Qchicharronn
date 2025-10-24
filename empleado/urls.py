from django.urls import path,include
from empleado.views import *

app_name = 'empleado'

urlpatterns = [
    path('listar/', EmpleadoListView.as_view(), name='listar_empleado'),
    path('crear/', EmpleadoCreateView.as_view(), name='crear_empleado'),
    path('editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='editar_empleado'),
    path('eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='eliminar_empleado'),
]