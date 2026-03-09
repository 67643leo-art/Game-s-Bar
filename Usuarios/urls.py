from django.urls import path
from .views import pageUsuario, ingresar_pagina

urlpatterns = [
    path("", pageUsuario),
    path('login/',ingresar_pagina)
]