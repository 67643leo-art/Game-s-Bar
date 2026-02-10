from django.urls import path
from . import views

urlpatterns = [
    path("Productos-gamebar", views.index)
]