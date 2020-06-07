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
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('new_cargo/', views.CargoCreateView.as_view(), name='new_cargo'),
    path('ret_cargo/<int:pk>/', views.RetrieveCargoView.as_view(), name='ret_cargo'),
    path('update_cargo/<int:pk>/', views.CargoUpdate.as_view(), name='update_cargo'),
    path('delete_cargo/<int:pk>/', views.CargoDelete.as_view(), name='delete_cargo'),
    path('preview_cargos/<int:pk>/', views.CargoDetailView.as_view(), name='preview_cargo'),
    path('preview_cargos/', views.CargoListView.as_view(), name='preview_cargos'),
    path('search_result/', views.CargoSearchListView.as_view(), name='search_result'),
    path('search_request/', views.SearchRequestView.as_view(), name='search_request')
]
