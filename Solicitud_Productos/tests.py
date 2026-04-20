from datetime import date

from django.test import TestCase

from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn

from .models import SolicitudProducto


class SolicitudProductoTests(TestCase):

    def setUp(self):
        self.proveedor = Proveedor_pxn.objects.create(
            empresa_prov="Games Supply",
            nombre_prov="Mario",
            contacto_prov="555123456"
        )
        self.producto = Producto_gb.objects.create(
            nombre_producto="Control Pro",
            cantidad=12,
            unidad_medida="pieza",
            proveedor=self.proveedor
        )

    def test_crear_solicitud_guarda_detalles_sin_modificar_stock(self):
        response = self.client.post("/pageSolicitudProductos/crear/", {
            "fecha": date(2026, 4, 15),
            "proveedor": self.proveedor.id,
            "estado": "Pendiente",
            "observaciones": "Pedido inicial",
            "nombre_producto[]": ["Control Pro", "Audifonos"],
            "categoria[]": ["Control", "Accesorio"],
            "cantidad[]": ["3", "5"],
        })

        self.assertEqual(response.status_code, 302)

        solicitud = SolicitudProducto.objects.get()
        self.assertEqual(solicitud.detalles.count(), 2)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 12)

    def test_actualizar_y_eliminar_solicitud_sin_modificar_stock(self):
        solicitud = SolicitudProducto.objects.create(
            folio="SOL-20260415-0001",
            fecha=date(2026, 4, 15),
            proveedor=self.proveedor,
            estado="Pendiente",
            observaciones="Original"
        )
        solicitud.detalles.create(
            nombre_producto="Control Pro",
            categoria="Control",
            cantidad=2
        )

        response = self.client.post(f"/pageSolicitudProductos/actualizar/{solicitud.id}/", {
            "fecha": date(2026, 4, 20),
            "proveedor": self.proveedor.id,
            "estado": "En proceso",
            "observaciones": "Actualizada",
            "nombre_producto[]": ["Control Elite"],
            "categoria[]": ["Control"],
            "cantidad[]": ["4"],
        })

        self.assertEqual(response.status_code, 302)

        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado, "En proceso")
        self.assertEqual(solicitud.detalles.count(), 1)
        self.assertEqual(solicitud.detalles.first().nombre_producto, "Control Elite")

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 12)

        detalle_response = self.client.get(f"/pageSolicitudProductos/ver/{solicitud.id}/")
        self.assertEqual(detalle_response.status_code, 200)
        self.assertContains(detalle_response, "Control Elite")

        delete_response = self.client.get(f"/pageSolicitudProductos/eliminar/{solicitud.id}/")
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(SolicitudProducto.objects.filter(id=solicitud.id).exists())
