from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Entrada
from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn


def inicio(request):

    entradas = Entrada.objects.all()
    proveedores = Proveedor_pxn.objects.all()

    return render(request, "entradaSalida.html", {
        'entradas': entradas,
        'proveedores': proveedores
    })


def buscar_productos(request):
    """Busca productos por letra o texto"""
    q = request.GET.get('q', '').strip()
    
    if len(q) < 1:
        return JsonResponse([])
    
    # Buscar productos que contengan la letra/texto (case-insensitive)
    productos = Producto_gb.objects.filter(
        nombre_producto__icontains=q
    ).values_list('nombre_producto', flat=True).distinct()
    
    # Convertir a lista y retornar como JSON
    return JsonResponse(list(productos), safe=False)


def agregar_entrada(request):

    if request.method == "POST":

        nombre_producto = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        unidad = request.POST.get("unidad_medida")
        proveedor_id = request.POST.get("proveedor")
        fecha = request.POST.get("fecha")

        proveedor = Proveedor_pxn.objects.get(id=proveedor_id)

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


def buscar_productos(request):
    """
    Vista para autocompletado de productos
    """
    query = request.GET.get('q', '').strip()

    if len(query) >= 1:
        productos = Producto_gb.objects.filter(
            nombre_producto__icontains=query
        ).values_list('nombre_producto', flat=True).distinct()[:10]  # Limitar a 10 resultados
    else:
        productos = []

    return JsonResponse(list(productos), safe=False)

    """
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

    
    
    
    """
