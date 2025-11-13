from nomina.views import *
from django.urls import path

app_name = 'nomina'
urlpatterns = [
    # _________________________ Modulos de Nomina __________________________
    path('listar/', NominaListView.as_view(), name='nomina_list'),
    path('crear/', NominaCreateView.as_view(), name='crear_nomina'),
    path('editar/<int:pk>', NominaUpdateView.as_view(), name='editar_nomina'),
    path('eliminar/<int:pk>', NominaDeleteView.as_view(), name='eliminar_nomina'),

]