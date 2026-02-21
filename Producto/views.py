from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Productos (request):
    return render(request,'Producto.html')