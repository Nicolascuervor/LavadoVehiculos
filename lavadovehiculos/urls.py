# lavadovehiculos/urls.py
"""
URL configuration for lavadovehiculos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/secciones/', include('secciones.urls')),  # URLs de la app secciones (APIs)
    path('', include('perfiles.urls')),  # URLs de la app perfiles (plantillas y APIs)
    path('login/', LoginView.as_view(template_name='perfiles/login.html'), name='login'),  # Vista de inicio de sesión
    path('logout/', LogoutView.as_view(), name='logout'),  # Vista de cierre de sesión,
    path('admins/', include('admins.urls')),  # Agrega la app admins
]

# Servir archivos estáticos y multimedia solo en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)