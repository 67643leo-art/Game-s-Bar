from django.urls import path
from .views import inicio, agregar_entrada, buscar_productos
urlpatterns = [

    path('', inicio),

    path('agregar_entrada/', agregar_entrada),

    path('buscar_productos/', buscar_productos)

]
