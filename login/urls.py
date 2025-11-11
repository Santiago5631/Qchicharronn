from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.Login_view.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
]