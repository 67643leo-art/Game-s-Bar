from django.db import models

class Proveedor_pxn(models.Model):
    empresa_prov = models.CharField(max_length=50)
    nombre_prov = models.CharField(max_length=50)
    contacto_prov = models.TextField(max_length=100)
    
    def __str__(self):
        return self.nombre_prov