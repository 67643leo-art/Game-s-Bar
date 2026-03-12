from django.db import models
from Producto.models import Producto_gb
from Proveedor.models import Proveedor_pxn


class Entrada(models.Model):

    producto = models.ForeignKey(
        Producto_gb,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField()

    unidad_medida = models.CharField(
        max_length=10,
        choices=[
            ('kg','kg'),
            ('pieza','pieza'),
            ('caja','caja'),
            ('litro','litro')
        ]
    )

    proveedor = models.ForeignKey(
        Proveedor_pxn,
        on_delete=models.CASCADE
    )

    fecha = models.DateField()

    def __str__(self):
        return f"Entrada {self.producto} - {self.cantidad}"
