from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Proveedor (request):
    return render(request,'Proveedor.html')