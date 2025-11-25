from informe.views import *
from django.urls import path

app_name = 'informe'
urlpatterns = [

    # -------------------- Informe --------------------
    path('listar/', InformeListView.as_view(), name='informe_list'),
    path('crear/', InformeCreateView.as_view(), name='crear_informe'),
    path('editar/<int:pk>/', InformeUpdateView.as_view(), name='editar_informe'),
    path('eliminar/<int:pk>/', InformeDeleteView.as_view(), name='eliminar_informe'),
    path('exportar/excel/', exportar_excel, name='exportar_excel'),
    path('exportar/pdf/', exportar_pdf, name='exportar_pdf'),

]
