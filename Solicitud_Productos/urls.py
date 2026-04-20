from django.urls import path
from .views import (
    Solicitud_Productos,
    actualizar_solicitud,
    crear_solicitud,
    detalle_solicitud,
    editar_solicitud,
    eliminar_solicitud,
)

urlpatterns = [
    path("", Solicitud_Productos),
    path("crear/", crear_solicitud),
    path("ver/<int:id>/", detalle_solicitud),
    path("editar/<int:id>/", editar_solicitud),
    path("actualizar/<int:id>/", actualizar_solicitud),
    path("eliminar/<int:id>/", eliminar_solicitud),
]
