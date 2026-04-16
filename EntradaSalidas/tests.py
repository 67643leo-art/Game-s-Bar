from datetime import date

from django.test import TestCase

from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn
from Sucursal.models import Sucursal

from .models import Salida


class SalidaTests(TestCase):

    def setUp(self):
        self.proveedor = Proveedor_pxn.objects.create(
            empresa_prov="Games Supply",
            nombre_prov="Mario",
            contacto_prov="555123456"
        )
        self.producto = Producto_gb.objects.create(
            nombre_producto="Papas",
            cantidad=10,
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

    def test_agregar_salida_resta_stock_y_crea_registro(self):
        response = self.client.post("/pageEntradasSalidas/agregar_salida/", {
            "producto": self.producto.id,
            "cantidad": 3,
            "sucursal": self.sucursal.id,
            "fecha": date(2026, 4, 14)
        })

        self.assertEqual(response.status_code, 302)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 7)

        salida = Salida.objects.get()
        self.assertEqual(salida.producto, self.producto)
        self.assertEqual(salida.sucursal, self.sucursal)
        self.assertEqual(salida.cantidad, 3)

    def test_detalle_sucursal_muestra_resumen_de_productos(self):
        Salida.objects.create(
            producto=self.producto,
            cantidad=2,
            unidad_medida=self.producto.unidad_medida,
            sucursal=self.sucursal,
            fecha=date(2026, 4, 13)
        )
        Salida.objects.create(
            producto=self.producto,
            cantidad=3,
            unidad_medida=self.producto.unidad_medida,
            sucursal=self.sucursal,
            fecha=date(2026, 4, 14)
        )

        response = self.client.get(f"/pageSucursal/detalleSucursal/{self.sucursal.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Papas")
        self.assertEqual(response.context["productos_recibidos"][0]["total_recibido"], 5)
