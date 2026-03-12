from django.urls import path
from . import views

urlpatterns = [
    path('', views.Sucursal, name='Sucursal'),
    path('sumar_sucursal/', views.sumar_sucursal, name='sumar_sucursal'),
    path('eliminar_sucursal/<int:id>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    path('editar_sucursal/<int:id>/', views.editar_sucursal, name='editar_sucursal'),
    path('actualizar_sucursal/<int:id>/', views.actualizar_sucursal, name='actualizar_sucursal'),
]