from django.urls import path
from .views import Productos

urlpatterns = [
    path('',Productos)
]