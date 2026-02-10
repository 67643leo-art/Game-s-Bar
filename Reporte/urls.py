from django.urls import path
from . import views

urlpatterns = [
    path("Reporte-gamebar", views.index)
]