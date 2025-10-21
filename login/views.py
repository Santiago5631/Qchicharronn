from django.contrib.auth.views import LoginView

#logica login 

class Login_view(LoginView):
    template_name = 'login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context["titulo"] = "Iniciar Sesion"
        return context
    
def custom_logout_view(request):
    logout(request)
    return redirect('login')