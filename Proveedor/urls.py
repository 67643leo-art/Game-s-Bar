from django.urls import path
from .views import Proveedor

urlpatterns = [
    path('',Proveedor)
]