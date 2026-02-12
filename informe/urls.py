from django.urls import path
from .views import informe_list

app_name = 'informe'

urlpatterns = [
    path('listar/', informe_list, name='informe_list'),
]