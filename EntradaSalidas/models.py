from django.db import models
from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn
from Sucursal.models import Sucursal


UNIDADES_MEDIDA = [
    ('kg', 'kg'),
    ('pieza', 'pieza'),
    ('caja', 'caja'),
    ('litro', 'litro')
]


class Entrada(models.Model):

    producto = models.ForeignKey(
        Producto_gb,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField(default=0)

    unidad_medida = models.CharField(
        max_length=10,
        choices=UNIDADES_MEDIDA
    )

    proveedor = models.ForeignKey(
        Proveedor_pxn,
        on_delete=models.CASCADE
    )

    fecha = models.DateField()

    def __str__(self):
        return f"Entrada {self.producto} - {self.cantidad}"


class Salida(models.Model):

    producto = models.ForeignKey(
        Producto_gb,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField(default=0)

    unidad_medida = models.CharField(
        max_length=10,
        choices=UNIDADES_MEDIDA
    )

    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='salidas'
    )

    fecha = models.DateField()

    def __str__(self):
        return f"Salida {self.producto} - {self.cantidad}"
