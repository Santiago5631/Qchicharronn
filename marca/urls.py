from marca.views import *
from django.urls import path

app_name = 'menu'
urlpatterns = [
    # -------------------- Marca --------------------
    path('listar/', MarcaListView.as_view(), name='marca_list'),
    path('crear/', MarcaCreateView.as_view(), name='marca_create'),
    path('actualizar/<int:pk>/', MarcaUpdateView.as_view(), name='marca_update'),
    path('eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_delete'),

]