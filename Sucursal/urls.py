from django.urls import path
from . import views

urlpatterns = [
    path("Sucursal-gamebar", views.index)
]