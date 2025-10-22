from django.urls import path,include
from empleado.views import *

urlpatterns = [
    path('empleados/listar/', EmpleadoListView.as_view(), name='listar_empleado'),
    path('empleados/crear/', EmpleadoCreateView.as_view(), name='crear_empleado'),
    path('empleados/editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='editar_empleado'),
    path('empleados/eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='eliminar_empleado'),
]