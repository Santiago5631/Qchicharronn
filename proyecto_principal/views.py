from django.shortcuts import render
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'public/home.html')
def dashboard(request):
    return render(request, 'dashboard/aside/Dashboard.html')


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard/aside/Dashboard.html')