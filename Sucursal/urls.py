from django.urls import path
from .views import Sucursal

urlpatterns = [
    path("", Sucursal)
]