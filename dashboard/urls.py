"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html', views.about, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('charts.html', views.charts, name='charts'),
    path('', views.service_bus_view, name='service_bus_view'),
    #path('stream/',views.stream,name="stream"),

    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
