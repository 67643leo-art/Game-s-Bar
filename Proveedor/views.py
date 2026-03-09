from django.shortcuts import render,redirect
from .models import Proveedor_pxn
# Create your views here.
def Proveedor (request):
    return render(request,'Proveedor.html')

def sumar_proveedor(request):
    provedor = Proveedor_pxn(
        empresa = request.POST['empresa_prov'],
        nprovedor = request.POST['nombre_prov'],
        conatco = request.POST['contacto_prov']
    )
    provedor.save()
    return redirect('/pageProveedores/')