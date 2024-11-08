"""
URL configuration for saapy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from health import views
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'health', views.HealthViewSet)

urlpatterns = [

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('auth/', views.auth_view),
    path('home/', views.home),
    path('logindetails/', views.logindetails),
    path('login/', views.login),
    path('logout/', views.logout),
    path('pdetails/', views.pdetails),
    path('formsubmit/', views.formsubmit),
    path('archive/', views.archive),
    path('process/',views.generate_chart),
    path('send_email/',views.send_email),
path('', lambda request: redirect('login/', permanent=True)),
    
]
