from django.urls import path, include
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
]