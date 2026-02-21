from django.urls import path
from .views import Solicitud_Productos

urlpatterns = [
    path(" ", Solicitud_Productos)
]