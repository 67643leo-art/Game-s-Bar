<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal

def pageSucursal(request):

    sucursales = Sucursal.objects.all()

    return render(request, "sucursal.html", {
        "sucursales": sucursales
    })

def crearSucursal(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        direccion = request.POST.get("direccion")
        ciudad = request.POST.get("ciudad")
        telefono = request.POST.get("telefono")
        encargado = request.POST.get("encargado")
        email = request.POST.get("email")
        horario = request.POST.get("horario")
        estado = request.POST.get("estado")

        Sucursal.objects.create(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            encargado=encargado,
            email=email,
            horario=horario,
            estado=estado
        )

    return redirect("/pageSucursal/")


def editarSucursal(request, id):

    sucursal = get_object_or_404(Sucursal, id=id)

    if request.method == "POST":

        sucursal.nombre = request.POST.get("nombre")
        sucursal.direccion = request.POST.get("direccion")
        sucursal.ciudad = request.POST.get("ciudad")
        sucursal.telefono = request.POST.get("telefono")
        sucursal.encargado = request.POST.get("encargado")
        sucursal.email = request.POST.get("email")
        sucursal.horario = request.POST.get("horario")
        sucursal.estado = request.POST.get("estado")

        sucursal.save()

        return redirect("/pageSucursal/")

    return render(request,"editarSucursal.html", {
        "sucursal": sucursal
    })

def eliminarSucursal(request, id):

    sucursal = get_object_or_404(Sucursal, id=id)

    sucursal.delete()

    return redirect("/pageSucursal/")
>>>>>>> bab294d71edd8fa96fbef62573f93678978f6ea2
