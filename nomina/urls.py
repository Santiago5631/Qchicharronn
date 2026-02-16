from django.urls import path
from . import views

app_name = 'nomina'

urlpatterns = [
    path('listar/', views.NominaListView.as_view(), name='nomina_list'),
    path('crear/', views.NominaCreateView.as_view(), name='crear_nomina'),
    path('editar/<int:pk>/', views.NominaUpdateView.as_view(), name='editar_nomina'),
    path('eliminar/<int:pk>/', views.NominaDeleteView.as_view(), name='eliminar_nomina'),
    path('pdf/', views.generar_pdf_nomina, name='nomina_pdf'),
]
