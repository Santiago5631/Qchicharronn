from marca.views import *
from django.urls import path

app_name = 'menu'
urlpatterns = [
    # -------------------- Marca --------------------
    path('marcas/listar/', MarcaListView.as_view(), name='marca_list'),
    path('marcas/crear/', MarcaCreateView.as_view(), name='marca_create'),
    path('marcas/actualizar/<int:pk>/', MarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_delete'),

]