from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Usuario (request):
    return render(request,"Usuario.html")
