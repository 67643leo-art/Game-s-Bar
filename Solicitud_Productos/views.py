from datetime import date

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from Proveedor.models import Proveedor_pxn

from .models import DetalleSolicitudProducto, SolicitudProducto


def _generar_folio(fecha_solicitud):
    consecutivo = SolicitudProducto.objects.filter(fecha=fecha_solicitud).count() + 1
    return f"SOL-{fecha_solicitud:%Y%m%d}-{consecutivo:04d}"


def _obtener_detalles_desde_post(request):
    nombres = request.POST.getlist('nombre_producto[]')
    categorias = request.POST.getlist('categoria[]')
    cantidades = request.POST.getlist('cantidad[]')

    detalles = []
    categorias_validas = {categoria for categoria, _ in DetalleSolicitudProducto.CATEGORIAS}

    for nombre, categoria, cantidad in zip(nombres, categorias, cantidades):
        nombre = nombre.strip()
        categoria = categoria.strip()
        cantidad = cantidad.strip()

        if not nombre and not categoria and not cantidad:
            continue

        if not nombre:
            raise ValueError("Cada detalle debe incluir el nombre del producto.")

        if categoria not in categorias_validas:
            raise ValueError("Selecciona una categoria valida para cada producto.")

        try:
            cantidad_int = int(cantidad)
        except ValueError as exc:
            raise ValueError("La cantidad de cada producto solicitado debe ser un numero entero.") from exc

        if cantidad_int <= 0:
            raise ValueError("La cantidad de cada producto solicitado debe ser mayor a cero.")

        detalles.append({
            'nombre_producto': nombre,
            'categoria': categoria,
            'cantidad': cantidad_int,
        })

    if not detalles:
        raise ValueError("Agrega al menos un producto a la solicitud.")

    return detalles


def _construir_contexto(form_data=None, solicitud_editar=None):
    solicitudes = SolicitudProducto.objects.select_related('proveedor').prefetch_related('detalles').order_by('-fecha', '-id')
    proveedores = Proveedor_pxn.objects.all().order_by('empresa_prov')
    estado_opciones = [estado for estado, _ in SolicitudProducto.ESTADOS]
    categoria_opciones = [categoria for categoria, _ in DetalleSolicitudProducto.CATEGORIAS]

    if form_data is None:
        if solicitud_editar is not None:
            form_data = {
                'folio': solicitud_editar.folio,
                'fecha': solicitud_editar.fecha.isoformat(),
                'proveedor_id': solicitud_editar.proveedor_id,
                'estado': solicitud_editar.estado,
                'observaciones': solicitud_editar.observaciones,
                'detalles': [
                    {
                        'nombre_producto': detalle.nombre_producto,
                        'categoria': detalle.categoria,
                        'cantidad': detalle.cantidad,
                    }
                    for detalle in solicitud_editar.detalles.all()
                ] or [{
                    'nombre_producto': '',
                    'categoria': 'Videojuego',
                    'cantidad': '',
                }]
            }
        else:
            fecha_hoy = date.today()
            form_data = {
                'folio': _generar_folio(fecha_hoy),
                'fecha': fecha_hoy.isoformat(),
                'proveedor_id': '',
                'estado': 'Pendiente',
                'observaciones': '',
                'detalles': [{
                    'nombre_producto': '',
                    'categoria': 'Videojuego',
                    'cantidad': '',
                }]
            }

    return {
        'solicitudes': solicitudes,
        'proveedores': proveedores,
        'estado_opciones': estado_opciones,
        'categoria_opciones': categoria_opciones,
        'form_data': form_data,
        'solicitud_editar': solicitud_editar,
    }


def Solicitud_Productos(request):
    return render(request, "Solicitud_Productos.html", _construir_contexto())


def crear_solicitud(request):
    if request.method != "POST":
        return redirect("/pageSolicitudProductos/")

    fecha_texto = request.POST.get('fecha', '').strip()
    proveedor_id = request.POST.get('proveedor', '').strip()
    estado = request.POST.get('estado', 'Pendiente').strip() or 'Pendiente'
    observaciones = request.POST.get('observaciones', '').strip()

    form_data = {
        'folio': request.POST.get('folio', '').strip(),
        'fecha': fecha_texto,
        'proveedor_id': proveedor_id,
        'estado': estado,
        'observaciones': observaciones,
        'detalles': [
            {
                'nombre_producto': nombre,
                'categoria': categoria,
                'cantidad': cantidad,
            }
            for nombre, categoria, cantidad in zip(
                request.POST.getlist('nombre_producto[]'),
                request.POST.getlist('categoria[]'),
                request.POST.getlist('cantidad[]')
            )
        ] or [{
            'nombre_producto': '',
            'categoria': 'Videojuego',
            'cantidad': '',
        }]
    }

    try:
        if not fecha_texto or not proveedor_id:
            raise ValueError("Completa la fecha y el proveedor de la solicitud.")

        fecha_solicitud = date.fromisoformat(fecha_texto)
        proveedor = Proveedor_pxn.objects.get(id=proveedor_id)
        detalles = _obtener_detalles_desde_post(request)
    except (Proveedor_pxn.DoesNotExist, ValueError) as exc:
        messages.error(request, str(exc))
        return render(request, "Solicitud_Productos.html", _construir_contexto(form_data=form_data))

    with transaction.atomic():
        solicitud = SolicitudProducto.objects.create(
            folio=_generar_folio(fecha_solicitud),
            fecha=fecha_solicitud,
            proveedor=proveedor,
            estado=estado,
            observaciones=observaciones,
        )
        DetalleSolicitudProducto.objects.bulk_create([
            DetalleSolicitudProducto(
                solicitud=solicitud,
                nombre_producto=detalle['nombre_producto'],
                categoria=detalle['categoria'],
                cantidad=detalle['cantidad'],
            )
            for detalle in detalles
        ])

    messages.success(request, "La solicitud de productos se guardo correctamente.")
    return redirect("/pageSolicitudProductos/")


def editar_solicitud(request, id):
    solicitud = get_object_or_404(
        SolicitudProducto.objects.select_related('proveedor').prefetch_related('detalles'),
        id=id
    )
    return render(
        request,
        "Solicitud_Productos.html",
        _construir_contexto(solicitud_editar=solicitud)
    )


def actualizar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudProducto.objects.select_related('proveedor').prefetch_related('detalles'), id=id)

    if request.method != "POST":
        return redirect("/pageSolicitudProductos/")

    fecha_texto = request.POST.get('fecha', '').strip()
    proveedor_id = request.POST.get('proveedor', '').strip()
    estado = request.POST.get('estado', 'Pendiente').strip() or 'Pendiente'
    observaciones = request.POST.get('observaciones', '').strip()

    form_data = {
        'folio': solicitud.folio,
        'fecha': fecha_texto,
        'proveedor_id': proveedor_id,
        'estado': estado,
        'observaciones': observaciones,
        'detalles': [
            {
                'nombre_producto': nombre,
                'categoria': categoria,
                'cantidad': cantidad,
            }
            for nombre, categoria, cantidad in zip(
                request.POST.getlist('nombre_producto[]'),
                request.POST.getlist('categoria[]'),
                request.POST.getlist('cantidad[]')
            )
        ] or [{
            'nombre_producto': '',
            'categoria': 'Videojuego',
            'cantidad': '',
        }]
    }

    try:
        if not fecha_texto or not proveedor_id:
            raise ValueError("Completa la fecha y el proveedor de la solicitud.")

        fecha_solicitud = date.fromisoformat(fecha_texto)
        proveedor = Proveedor_pxn.objects.get(id=proveedor_id)
        detalles = _obtener_detalles_desde_post(request)
    except (Proveedor_pxn.DoesNotExist, ValueError) as exc:
        messages.error(request, str(exc))
        return render(
            request,
            "Solicitud_Productos.html",
            _construir_contexto(form_data=form_data, solicitud_editar=solicitud)
        )

    with transaction.atomic():
        solicitud.fecha = fecha_solicitud
        solicitud.proveedor = proveedor
        solicitud.estado = estado
        solicitud.observaciones = observaciones
        solicitud.save()

        solicitud.detalles.all().delete()
        DetalleSolicitudProducto.objects.bulk_create([
            DetalleSolicitudProducto(
                solicitud=solicitud,
                nombre_producto=detalle['nombre_producto'],
                categoria=detalle['categoria'],
                cantidad=detalle['cantidad'],
            )
            for detalle in detalles
        ])

    messages.success(request, "La solicitud de productos se actualizo correctamente.")
    return redirect("/pageSolicitudProductos/")


def detalle_solicitud(request, id):
    solicitud = get_object_or_404(
        SolicitudProducto.objects.select_related('proveedor').prefetch_related('detalles'),
        id=id
    )
    return render(request, "detalleSolicitudProducto.html", {
        'solicitud': solicitud
    })


def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudProducto, id=id)
    solicitud.delete()
    messages.success(request, "La solicitud de productos se elimino correctamente.")
    return redirect("/pageSolicitudProductos/")
