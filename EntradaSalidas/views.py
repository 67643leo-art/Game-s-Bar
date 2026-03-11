from django.shortcuts import render, redirect
from .models import Entrada
from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn


def inicio(request):

    entradas = Entrada.objects.all()

    return render(request, "entradaSalida.html", {
        'entradas': entradas
    })


def agregar_entrada(request):

    if request.method == "POST":

        nombre_producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        unidad = request.POST.get("unidad_medida")
        nombre_proveedor = request.POST.get("proveedor")
        fecha = request.POST.get("fecha")

        # Crear proveedor si no existe
        proveedor, creado = Proveedor_pxn.objects.get_or_create(
            empresa_prov=nombre_proveedor
        )

        # Crear producto si no existe
        producto, creado = Producto_gb.objects.get_or_create(
            nombre_producto=nombre_producto,
            defaults={
                'cantidad': cantidad,
                'unidad_medida': unidad,
                'proveedor': proveedor
            }
        )

        # Crear entrada
        Entrada.objects.create(
            producto=producto,
            cantidad=cantidad,
            unidad_medida=unidad,
            proveedor=proveedor,
            fecha=fecha
        )

    return redirect("/pageEntradasSalidas/")


def actualizar_entrada(request, id):

    entrada = Entrada.objects.get(id=id)

    if request.method == "POST":

        entrada.producto.nombre_producto = request.POST.get("producto")
        entrada.cantidad = request.POST.get("cantidad")
        entrada.unidad_medida = request.POST.get("unidad_medida")
        entrada.proveedor.empresa_prov = request.POST.get("proveedor")
        entrada.fecha = request.POST.get("fecha")

        entrada.producto.save()
        entrada.proveedor.save()
        entrada.save()

        return redirect("/pageEntradasSalidas/")

    return render(request, "entradaSalida.html", {
        "entrada": entrada,
        "entradas": Entrada.objects.all()
    })
