from multiprocessing.resource_tracker import register

from  django.urls import path
from login.views import *

urlpatterns = [
    path('', Login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]