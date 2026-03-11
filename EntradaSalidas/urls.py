from django.urls import path
from .views import inicio, agregar_entrada, actualizar_entrada

urlpatterns = [

    path('', inicio),

    path('agregar_entrada/', agregar_entrada),

    path('actualizar_entrada/<int:id>/', actualizar_entrada),

]
