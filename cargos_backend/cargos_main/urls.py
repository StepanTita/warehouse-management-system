"""cargos_backend URL Configuration

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
from django.urls import path, include
from . import views
from django.views.generic import ListView, DetailView, DeleteView
from .models import Cargo
from .util_vars import last_cargos

urlpatterns = [
    path('', views.index, name='index'),
    path('new_cargo/', views.new_cargo, name='new_cargo'),
    path('preview_cargos/', ListView.as_view(queryset=Cargo.objects.all().order_by("-date_added")[:last_cargos],
                                             template_name='preview_cargos/preview_cargos.html'),
         name='preview_cargos'),
    path('preview_cargos/<pk>/', DetailView.as_view(model=Cargo,
                                                           template_name='preview_cargos/preview_cargo.html'),
         name='preview_cargo'),
    path('ret_cargo/', views.ret_cargo, name='ret_cargo'),
]
