from django.urls import path
from .views import reporte, generar_reporte

urlpatterns = [
    path("", reporte),
    path("generar_reporte/", generar_reporte)
]