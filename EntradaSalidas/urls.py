from django.urls import path
from .views import agregar_entrada, agregar_salida, inicio
urlpatterns = [

    path('', inicio),

    path('agregar_entrada/', agregar_entrada),

    path('agregar_salida/', agregar_salida)

]
