from django.shortcuts import render, redirect
from .models import Sucursal_pxn

def Sucursal(request):
    sucursales = Sucursal_pxn.objects.all()
    return render(request, "Sucursal.html", {"sucursales": sucursales})

def sumar_sucursal(request):
    if request.method == "POST":
        sucursal = Sucursal_pxn(
            nombre_suc=request.POST['nombre_suc'],
            direccion_suc=request.POST['direccion_suc'],
            ciudad_suc=request.POST['ciudad_suc'],
            telefono_suc=request.POST.get('telefono_suc', ''),
            encargado_suc=request.POST.get('encargado_suc', ''),
            email_suc=request.POST.get('email_suc', ''),
            horario_suc=request.POST.get('horario_suc', ''),
            estado_suc=request.POST.get('estado_suc', 'Activo'),
            empleados_suc=request.POST.get('empleados_suc', 0)
        )
        sucursal.save()
    return redirect('/pageSucursal/')

def eliminar_sucursal(request, id):
    sucursal = Sucursal_pxn.objects.get(id=id)
    sucursal.delete()
    return redirect('/pageSucursal/')

def editar_sucursal(request, id):
    sucursal = Sucursal_pxn.objects.get(id=id)
    return render(request, "Sucursal.html", {"sucursal": sucursal})

def actualizar_sucursal(request, id):
    sucursal = Sucursal_pxn.objects.get(id=id)
    if request.method == "POST":
        sucursal.nombre_suc = request.POST['nombre_suc']
        sucursal.direccion_suc = request.POST['direccion_suc']
        sucursal.ciudad_suc = request.POST['ciudad_suc']
        sucursal.telefono_suc = request.POST.get('telefono_suc', '')
        sucursal.encargado_suc = request.POST.get('encargado_suc', '')
        sucursal.email_suc = request.POST.get('email_suc', '')
        sucursal.horario_suc = request.POST.get('horario_suc', '')
        sucursal.estado_suc = request.POST.get('estado_suc', 'Activo')
        sucursal.empleados_suc = request.POST.get('empleados_suc', 0)
        sucursal.save()
    return redirect('/pageSucursal/')