from django.db.models import Max, Sum
from django.shortcuts import get_object_or_404, redirect, render

from EntradaSalidas.models import Salida

from .models import Sucursal


def pageSucursal(request):

    sucursales = Sucursal.objects.all().order_by('nombre')

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


def detalleSucursal(request, id):

    sucursal = get_object_or_404(Sucursal, id=id)

    salidas = Salida.objects.filter(sucursal=sucursal).select_related('producto').order_by('-fecha', '-id')

    productos_recibidos = salidas.values(
        'producto__id',
        'producto__nombre_producto',
        'unidad_medida'
    ).annotate(
        total_recibido=Sum('cantidad'),
        ultima_fecha=Max('fecha')
    ).order_by('producto__nombre_producto')

    return render(request, "detalleSucursal.html", {
        "sucursal": sucursal,
        "salidas": salidas,
        "productos_recibidos": productos_recibidos
    })
