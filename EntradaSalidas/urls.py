from django.urls import path
from . import views

urlpatterns = [
    path("EntradaSalida-gamebar", views.index)
]