# buscador/urls.py
from django.urls import path
from .views import buscar, buscar2

urlpatterns = [
    path('mi_buscador/', buscar, name='buscar'),
    path('mi_buscador2/', buscar2, name='buscar2'),
]
