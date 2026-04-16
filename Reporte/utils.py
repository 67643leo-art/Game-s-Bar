import csv
import io
import re
import zipfile
from xml.sax.saxutils import escape


def sanitize_filename(file_name, fallback='reporte_inventario'):
    cleaned = re.sub(r'[^A-Za-z0-9._-]+', '_', (file_name or '').strip())
    cleaned = cleaned.strip('._')
    return cleaned or fallback


def build_report_rows(
    *,
    year,
    file_name,
    format_name,
    incidencias,
    observaciones,
    total_entradas,
    total_salidas,
    total_stock_restante,
    productos_con_stock,
    entradas,
    salidas,
    stock_por_producto,
):
    rows = [
        ['Reporte de Inventario Game\'sBar'],
        ['Anio del periodo', year],
        ['Nombre del archivo', file_name],
        ['Formato de exportacion', format_name.upper()],
        [],
        ['Resumen del periodo'],
        ['Total de entradas registradas', total_entradas],
        ['Total de salidas registradas', total_salidas],
        ['Unidades restantes en matriz al cierre del anio', total_stock_restante],
        ['Productos con stock al cierre del anio', productos_con_stock],
        [],
        ['Incidencias del producto'],
        [incidencias or 'Sin incidencias registradas.'],
        [],
        ['Observaciones generales'],
        [observaciones or 'Sin observaciones registradas.'],
        [],
        ['Detalle de entradas'],
        ['ID', 'Fecha', 'Producto', 'Cantidad', 'Unidad', 'Proveedor'],
    ]

    if entradas:
        rows.extend([
            [
                entrada.id,
                entrada.fecha.isoformat(),
                entrada.producto.nombre_producto,
                entrada.cantidad,
                entrada.unidad_medida,
                entrada.proveedor.empresa_prov,
            ]
            for entrada in entradas
        ])
    else:
        rows.append(['No hay entradas registradas para este anio.'])

    rows.extend([
        [],
        ['Detalle de salidas'],
        ['ID', 'Fecha', 'Producto', 'Cantidad', 'Unidad', 'Sucursal'],
    ])

    if salidas:
        rows.extend([
            [
                salida.id,
                salida.fecha.isoformat(),
                salida.producto.nombre_producto,
                salida.cantidad,
                salida.unidad_medida,
                salida.sucursal.nombre,
            ]
            for salida in salidas
        ])
    else:
        rows.append(['No hay salidas registradas para este anio.'])

    rows.extend([
        [],
        ['Stock restante por producto al cierre del anio'],
        ['Producto', 'Stock restante', 'Unidad'],
    ])

    if stock_por_producto:
        rows.extend([
            [producto['nombre_producto'], producto['stock_restante'], producto['unidad_medida']]
            for producto in stock_por_producto
        ])
    else:
        rows.append(['No hay stock acumulado para este anio.'])

    return rows


def export_csv(rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    return output.getvalue().encode('utf-8-sig')


def export_xlsx(rows, sheet_name='Reporte'):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

    workbook = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""

    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
  <fills count="2">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
  </fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""

    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:creator>Game'sBar</dc:creator>
  <cp:lastModifiedBy>Game'sBar</cp:lastModifiedBy>
</cp:coreProperties>"""

    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Game'sBar</Application>
</Properties>"""

    worksheet_rows = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for col_index, value in enumerate(row, start=1):
            cell_ref = f"{_column_letter(col_index)}{row_index}"
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                cells.append(f'<c r="{cell_ref}"><v>{value}</v></c>')
            else:
                text = escape(str(value))
                cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{text}</t></is></c>')
        worksheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    worksheet = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    {''.join(worksheet_rows)}
  </sheetData>
</worksheet>"""

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('xl/workbook.xml', workbook)
        zf.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        zf.writestr('xl/worksheets/sheet1.xml', worksheet)
        zf.writestr('xl/styles.xml', styles)
        zf.writestr('docProps/core.xml', core)
        zf.writestr('docProps/app.xml', app)
    return buffer.getvalue()


def export_pdf(lines):
    if not lines:
        lines = ['Reporte vacio']

    page_height = 842
    top_y = 800
    left_x = 50
    line_height = 14
    max_lines_per_page = 50
    paginated_lines = [lines[i:i + max_lines_per_page] for i in range(0, len(lines), max_lines_per_page)]

    objects = [None, None, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    page_refs = []

    for page_lines in paginated_lines:
        content_lines = [
            "BT",
            "/F1 10 Tf",
            f"{left_x} {top_y} Td",
            f"{line_height} TL",
        ]

        for index, raw_line in enumerate(page_lines):
            safe_line = _pdf_escape(raw_line)
            if index == 0:
                content_lines.append(f"({safe_line}) Tj")
            else:
                content_lines.append("T*")
                content_lines.append(f"({safe_line}) Tj")

        content_lines.append("ET")
        stream = "\n".join(content_lines).encode('latin-1', 'replace')
        content_id = len(objects) + 1
        objects.append(f"<< /Length {len(stream)} >>\nstream\n{stream.decode('latin-1')}\nendstream")

        page_id = len(objects) + 1
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 {page_height}] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>"
        )
        page_refs.append(f"{page_id} 0 R")

    objects[1] = f"<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {len(page_refs)} >>"
    objects[0] = "<< /Type /Catalog /Pages 2 0 R >>"

    pdf = io.BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = [0]

    for index, obj in enumerate(objects, start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{index} 0 obj\n{obj}\nendobj\n".encode('latin-1'))

    xref_pos = pdf.tell()
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode('latin-1'))
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode('latin-1'))

    pdf.write(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF"
        ).encode('latin-1')
    )
    return pdf.getvalue()


def rows_to_pdf_lines(rows):
    lines = []
    for row in rows:
        if not row:
            lines.append('')
        elif len(row) == 1:
            lines.append(str(row[0]))
        else:
            lines.append(' | '.join(str(value) for value in row))
    return lines


def _column_letter(index):
    result = ''
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _pdf_escape(value):
    text = str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    return text.encode('latin-1', 'replace').decode('latin-1')
