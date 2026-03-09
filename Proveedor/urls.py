from django.urls import path
from .views import Proveedor, sumar_proveedor

urlpatterns = [
    path('',Proveedor),
    path('sumar_proveedor/',sumar_proveedor)
]