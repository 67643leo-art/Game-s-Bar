from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Entrada
from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn
from Sucursal.models import Sucursal

from .models import Entrada, Salida


def inicio(request):
    entradas = Entrada.objects.select_related('producto', 'proveedor').order_by('-fecha', '-id')
    salidas = Salida.objects.select_related('producto', 'sucursal').order_by('-fecha', '-id')
    proveedores = Proveedor_pxn.objects.all().order_by('empresa_prov')
    productos = Producto_gb.objects.select_related('proveedor').order_by('nombre_producto')
    sucursales = Sucursal.objects.all().order_by('nombre')

    return render(request, "entradaSalida.html", {
        'entradas': entradas,
        'salidas': salidas,
        'proveedores': proveedores,
        'productos': productos,
        'sucursales': sucursales,
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
    if request.method != "POST":
        return redirect("/pageEntradasSalidas/")

    producto_id = request.POST.get("producto")
    producto_nuevo = request.POST.get("producto_nuevo", "").strip()
    cantidad_texto = request.POST.get("cantidad", "").strip()
    unidad = request.POST.get("unidad_medida")
    proveedor_id = request.POST.get("proveedor")
    fecha = request.POST.get("fecha")

    if not cantidad_texto or not fecha:
        messages.error(request, "Completa la cantidad y la fecha para registrar la entrada.")
        return redirect("/pageEntradasSalidas/")

    try:
        cantidad = int(cantidad_texto)
    except ValueError:
        messages.error(request, "La cantidad de la entrada debe ser un numero entero.")
        return redirect("/pageEntradasSalidas/")

    if cantidad <= 0:
        messages.error(request, "La cantidad de la entrada debe ser mayor a cero.")
        return redirect("/pageEntradasSalidas/")

    if not producto_id and not producto_nuevo:
        messages.error(request, "Selecciona un producto existente o escribe un producto nuevo.")
        return redirect("/pageEntradasSalidas/")

    if producto_id:
        producto = Producto_gb.objects.select_related('proveedor').get(id=producto_id)
        producto.cantidad += cantidad
        producto.save(update_fields=['cantidad'])
        proveedor = producto.proveedor
        unidad = producto.unidad_medida
    else:
        if not proveedor_id or not unidad:
            messages.error(request, "Para un producto nuevo debes seleccionar proveedor y unidad.")
            return redirect("/pageEntradasSalidas/")

        proveedor = Proveedor_pxn.objects.get(id=proveedor_id)
        producto, creado = Producto_gb.objects.get_or_create(
            nombre_producto=producto_nuevo,
            defaults={
                'cantidad': cantidad,
                'unidad_medida': unidad,
                'proveedor': proveedor
            }
        )

        if not creado:
            producto.cantidad += cantidad
            producto.save(update_fields=['cantidad'])
            proveedor = producto.proveedor
            unidad = producto.unidad_medida

    Entrada.objects.create(
        producto=producto,
        cantidad=cantidad,
        unidad_medida=unidad,
        proveedor=proveedor,
        fecha=fecha
    )

    messages.success(request, "La entrada se registro correctamente.")
    return redirect("/pageEntradasSalidas/")


def agregar_salida(request):
    if request.method != "POST":
        return redirect("/pageEntradasSalidas/")

    producto_id = request.POST.get("producto")
    cantidad_texto = request.POST.get("cantidad", "").strip()
    sucursal_id = request.POST.get("sucursal")
    fecha = request.POST.get("fecha")

    if not producto_id or not cantidad_texto or not sucursal_id or not fecha:
        messages.error(request, "Completa producto, cantidad, sucursal y fecha para registrar la salida.")
        return redirect("/pageEntradasSalidas/")

    try:
        cantidad = int(cantidad_texto)
    except ValueError:
        messages.error(request, "La cantidad de la salida debe ser un numero entero.")
        return redirect("/pageEntradasSalidas/")

    if cantidad <= 0:
        messages.error(request, "La cantidad de la salida debe ser mayor a cero.")
        return redirect("/pageEntradasSalidas/")

    with transaction.atomic():
        producto = Producto_gb.objects.select_for_update().get(id=producto_id)

        if cantidad > producto.cantidad:
            messages.error(
                request,
                f"No hay stock suficiente de {producto.nombre_producto}. Stock disponible: {producto.cantidad}."
            )
            return redirect("/pageEntradasSalidas/")

        sucursal = Sucursal.objects.get(id=sucursal_id)

        producto.cantidad -= cantidad
        producto.save(update_fields=['cantidad'])

        Salida.objects.create(
            producto=producto,
            cantidad=cantidad,
            unidad_medida=producto.unidad_medida,
            sucursal=sucursal,
            fecha=fecha
        )

    messages.success(request, "La salida se registro correctamente y el stock fue actualizado.")
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
