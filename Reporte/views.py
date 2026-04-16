from collections import defaultdict
from datetime import date

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from EntradaSalidas.models import Entrada, Salida

from .utils import (
    build_report_rows,
    export_csv,
    export_pdf,
    export_xlsx,
    rows_to_pdf_lines,
    sanitize_filename,
)


def reporte(request):
    context = _build_context()

    if request.method != "POST":
        return render(request, "reporte.html", context)

    anio_texto = request.POST.get('anio', '').strip()
    formato = request.POST.get('formato', '').strip().lower()
    nombre_archivo = request.POST.get('nombre_archivo', '').strip()
    incidencias = request.POST.get('incidencias', '').strip()
    observaciones = request.POST.get('observaciones', '').strip()

    context['form_data'] = {
        'anio': anio_texto,
        'formato': formato,
        'nombre_archivo': nombre_archivo,
        'incidencias': incidencias,
        'observaciones': observaciones,
    }

    try:
        if not anio_texto:
            raise ValueError("Ingresa el anio del periodo que deseas reportar.")

        anio = int(anio_texto)
        if anio < 2000 or anio > 2100:
            raise ValueError("El anio del periodo debe estar entre 2000 y 2100.")

        if formato not in {'pdf', 'xlsx', 'csv'}:
            raise ValueError("Selecciona un formato de exportacion valido.")
    except ValueError as exc:
        messages.error(request, str(exc))
        return render(request, "reporte.html", context)

    entradas = list(
        Entrada.objects.select_related('producto', 'proveedor')
        .filter(fecha__year=anio)
        .order_by('fecha', 'id')
    )
    salidas = list(
        Salida.objects.select_related('producto', 'sucursal')
        .filter(fecha__year=anio)
        .order_by('fecha', 'id')
    )

    total_entradas = sum(entrada.cantidad for entrada in entradas)
    total_salidas = sum(salida.cantidad for salida in salidas)
    stock_por_producto = _calcular_stock_por_producto(anio)
    total_stock_restante = sum(producto['stock_restante'] for producto in stock_por_producto)
    productos_con_stock = len(stock_por_producto)

    nombre_archivo_limpio = sanitize_filename(nombre_archivo or f"reporte_inventario_{anio}")

    rows = build_report_rows(
        year=anio,
        file_name=nombre_archivo_limpio,
        format_name=formato,
        incidencias=incidencias,
        observaciones=observaciones,
        total_entradas=total_entradas,
        total_salidas=total_salidas,
        total_stock_restante=total_stock_restante,
        productos_con_stock=productos_con_stock,
        entradas=entradas,
        salidas=salidas,
        stock_por_producto=stock_por_producto,
    )

    if formato == 'csv':
        content = export_csv(rows)
        response = HttpResponse(content, content_type='text/csv; charset=utf-8')
    elif formato == 'xlsx':
        content = export_xlsx(rows)
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        content = export_pdf(rows_to_pdf_lines(rows))
        response = HttpResponse(content, content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo_limpio}.{formato}"'
    return response


def _build_context():
    anios = sorted(
        set(Entrada.objects.values_list('fecha__year', flat=True)) |
        set(Salida.objects.values_list('fecha__year', flat=True))
    )

    anio_actual = date.today().year

    return {
        'anios_disponibles': anios,
        'form_data': {
            'anio': str(anio_actual),
            'formato': '',
            'nombre_archivo': f'reporte_inventario_{anio_actual}',
            'incidencias': '',
            'observaciones': '',
        }
    }


def _calcular_stock_por_producto(anio):
    fecha_corte = date(anio, 12, 31)
    stock = defaultdict(lambda: {
        'nombre_producto': '',
        'unidad_medida': '',
        'stock_restante': 0,
    })

    entradas_historicas = Entrada.objects.select_related('producto').filter(fecha__lte=fecha_corte)
    salidas_historicas = Salida.objects.select_related('producto').filter(fecha__lte=fecha_corte)

    for entrada in entradas_historicas:
        registro = stock[entrada.producto_id]
        registro['nombre_producto'] = entrada.producto.nombre_producto
        registro['unidad_medida'] = entrada.unidad_medida
        registro['stock_restante'] += entrada.cantidad

    for salida in salidas_historicas:
        registro = stock[salida.producto_id]
        registro['nombre_producto'] = salida.producto.nombre_producto
        registro['unidad_medida'] = salida.unidad_medida
        registro['stock_restante'] -= salida.cantidad

    return sorted(
        [registro for registro in stock.values() if registro['stock_restante'] > 0],
        key=lambda item: item['nombre_producto'].lower()
    )
