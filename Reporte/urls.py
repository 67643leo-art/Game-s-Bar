from django.urls import path
from .views import reporte

urlpatterns = [
    path("", reporte)
]