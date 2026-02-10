from django.urls import path
from . import views

urlpatterns = [
    path("Proveedores-gamebar", views.index)
]