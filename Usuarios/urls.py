from django.urls import path
from .views import Usuario

urlpatterns = [
    path("", Usuario)
]