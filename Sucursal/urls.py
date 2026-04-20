from django.urls import path
from .views import crearSucursal, detalleSucursal, editarSucursal, eliminarSucursal, pageSucursal

urlpatterns = [

    path("",pageSucursal),

    path("crearSucursal/",crearSucursal),

    path("editarSucursal/<int:id>/",editarSucursal),

    path("eliminarSucursal/<int:id>/",eliminarSucursal),

    path("detalleSucursal/<int:id>/", detalleSucursal),

]
