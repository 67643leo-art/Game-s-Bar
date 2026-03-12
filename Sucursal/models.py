from django.db import models

<<<<<<< HEAD
class Sucursal_pxn(models.Model):
    nombre_suc = models.CharField(max_length=100, verbose_name="Nombre de la Sucursal")
    direccion_suc = models.CharField(max_length=200, verbose_name="Dirección")
    ciudad_suc = models.CharField(max_length=100, verbose_name="Ciudad")
    telefono_suc = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    encargado_suc = models.CharField(max_length=100, blank=True, null=True, verbose_name="Encargado")
    email_suc = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Email")
    horario_suc = models.CharField(max_length=100, blank=True, null=True, verbose_name="Horario")
    estado_suc = models.CharField(max_length=20, default="Activo", verbose_name="Estado")
    empleados_suc = models.IntegerField(default=0, verbose_name="Número de Empleados")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    def __str__(self):
        return self.nombre_suc
    
    class Meta:
        db_table = 'sucursal'  # Esto hará que la tabla se llame 'sucursales' en DBeaver
=======

class Sucursal(models.Model):

    nombre = models.CharField(max_length=100)

    direccion = models.CharField(max_length=150)

    ciudad = models.CharField(max_length=100)

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    encargado = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    horario = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    ESTADO = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ]

    estado = models.CharField(
        max_length=10,
        choices=ESTADO,
        default='Activo'
    )

    def __str__(self):
        return self.nombre
>>>>>>> bab294d71edd8fa96fbef62573f93678978f6ea2
