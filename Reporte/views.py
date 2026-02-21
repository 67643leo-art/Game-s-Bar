from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def reporte (request): 
    return render(request, "reporte.html")