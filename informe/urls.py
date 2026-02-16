from informe.views import *
from django.urls import path
from django.views.generic import RedirectView

app_name = 'informe'
urlpatterns = [
    # Redirección automática de la raíz a listar
    path('', RedirectView.as_view(pattern_name='apl:informe:informe_list', permanent=False)),

    # Vista principal de reportes
    path('listar/', informe_list, name='informe_list'),

    # CRUD de informes (si se necesitan)
    path('crear/', InformeCreateView.as_view(), name='crear_informe'),
    path('editar/<int:pk>/', InformeUpdateView.as_view(), name='editar_informe'),
    path('eliminar/<int:pk>/', InformeDeleteView.as_view(), name='eliminar_informe'),
    path('exportar/excel/', exportar_excel, name='exportar_excel'),
    path('exportar/pdf/', exportar_pdf, name='exportar_pdf'),
]