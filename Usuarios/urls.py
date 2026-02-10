from django.urls import path
from . import views

urlpatterns = [
    path("Usuarios-gamebar", views.index)
]