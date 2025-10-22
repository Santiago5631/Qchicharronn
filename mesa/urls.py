from mesa.views import *
from django.urls import path

app_name = 'mesa'
urlpatterns = [

    # -------------------- Mesa --------------------
    path('mesas/', MesaListView.as_view(), name='mesa_list'),
    path('mesas/crear/', MesaCreateView.as_view(), name='crear_mesa'),
    path('mesas/editar/<int:pk>/', MesaUpdateView.as_view(), name='editar_mesa'),
    path('mesas/eliminar/<int:pk>/', MesaDeleteView.as_view(), name='eliminar_mesa'),

]