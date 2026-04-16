from datetime import date

from django.test import TestCase

from EntradaSalidas.models import Entrada, Salida
from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn
from Sucursal.models import Sucursal


class ReporteTests(TestCase):

    def setUp(self):
        self.proveedor = Proveedor_pxn.objects.create(
            empresa_prov="Games Supply",
            nombre_prov="Mario",
            contacto_prov="555123456"
        )
        self.producto = Producto_gb.objects.create(
            nombre_producto="Papas",
            cantidad=20,
            unidad_medida="caja",
            proveedor=self.proveedor
        )
        self.sucursal = Sucursal.objects.create(
            nombre="Sucursal Centro",
            direccion="Av Principal 123",
            ciudad="Leon",
            telefono="5551234567",
            encargado="Luisa",
            email="centro@gamesbar.com",
            horario="9 a 6",
            estado="Activo"
        )

        Entrada.objects.create(
            producto=self.producto,
            cantidad=10,
            unidad_medida="caja",
            proveedor=self.proveedor,
            fecha=date(2026, 1, 10)
        )
        Salida.objects.create(
            producto=self.producto,
            cantidad=4,
            unidad_medida="caja",
            sucursal=self.sucursal,
            fecha=date(2026, 2, 15)
        )
        Entrada.objects.create(
            producto=self.producto,
            cantidad=8,
            unidad_medida="caja",
            proveedor=self.proveedor,
            fecha=date(2027, 3, 1)
        )
        Salida.objects.create(
            producto=self.producto,
            cantidad=2,
            unidad_medida="caja",
            sucursal=self.sucursal,
            fecha=date(2027, 4, 2)
        )

    def test_reporte_filtra_movimientos_por_anio_en_csv(self):
        response = self.client.post("/pageReporte/", {
            "anio": 2027,
            "formato": "csv",
            "nombre_archivo": "reporte_2027",
            "incidencias": "Sin incidencias",
            "observaciones": "Revision anual"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])

        content = response.content.decode("utf-8-sig")
        self.assertIn("2027-03-01", content)
        self.assertIn("2027-04-02", content)
        self.assertNotIn("2026-01-10", content)
        self.assertNotIn("2026-02-15", content)

    def test_reporte_exporta_en_todos_los_formatos(self):
        formatos = {
            "csv": ("text/csv", b"\xef\xbb\xbf"),
            "xlsx": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", b"PK"),
            "pdf": ("application/pdf", b"%PDF"),
        }

        for formato, (content_type, magic_bytes) in formatos.items():
            response = self.client.post("/pageReporte/", {
                "anio": 2026,
                "formato": formato,
                "nombre_archivo": "reporte_prueba",
                "incidencias": "",
                "observaciones": ""
            })

            self.assertEqual(response.status_code, 200)
            self.assertIn(content_type, response["Content-Type"])
            self.assertIn(f'reporte_prueba.{formato}', response["Content-Disposition"])
            self.assertTrue(response.content.startswith(magic_bytes))
