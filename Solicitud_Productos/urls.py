from django.urls import path
from . import views

urlpatterns = [
    path("Solicitud-Productos-gamebar", views.index)
]