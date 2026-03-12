from django.urls import path
from .views import inicio, agregar_entrada
urlpatterns = [

    path('', inicio),

    path('agregar_entrada/', agregar_entrada)

]
