from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Sucursal(request):
    return render(request,"Sucursal.html")