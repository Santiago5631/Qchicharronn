from django.contrib import admin
from django.urls import path, include
from proyecto_principal import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('apps/', include('proyecto_principal.urls', namespace='apl')),

    #  CAMBIO AQUÍ
    path('login/', include('login.urls')),

    # Allauth
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
