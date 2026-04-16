from django.db import models

from Proveedor.models import Proveedor_pxn


class SolicitudProducto(models.Model):

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    folio = models.CharField(max_length=30, unique=True)
    fecha = models.DateField()
    proveedor = models.ForeignKey(
        Proveedor_pxn,
        on_delete=models.CASCADE,
        related_name='solicitudes_producto'
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Pendiente'
    )
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return self.folio


class DetalleSolicitudProducto(models.Model):

    CATEGORIAS = [
        ('Videojuego', 'Videojuego'),
        ('Consola', 'Consola'),
        ('Control', 'Control'),
        ('Accesorio', 'Accesorio'),
    ]

    solicitud = models.ForeignKey(
        SolicitudProducto,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    nombre_producto = models.CharField(max_length=100)
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS
    )
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.nombre_producto} - {self.cantidad}"
