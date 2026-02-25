from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Solicitud_Productos (request):
    return render(request,"Solicitud_Productos.html")
