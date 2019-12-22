from django.db import models
from Organizacion.models import PuntoDeConsumo
from Productos.models import ProductoGenerico
from django.utils import timezone


class Menu(models.Model):
    class Meta:
        verbose_name = 'Menú'
        verbose_name_plural = 'Menús'
    denominacion = models.CharField(max_length=60)
    fecha_actualizacion = models.DateField(default=timezone.now)
    PRIORIDAD = (
        ('Prioridad Alta', 'Prioridad Alta'),
        ('Prioridad Media', 'Prioridad Media'),
        ('Prioridad Baja', 'Prioridad Baja'),
    )
    prioridad = models.CharField(max_length=30, default='', choices=PRIORIDAD)

    def __str__(self):
        return self.denominacion

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.fecha_actualizacion = timezone.now()
        super(Menu, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)


class ComposicionMenu(models.Model):
    class Meta:
        verbose_name = 'Composicion Menú'
        verbose_name_plural = 'Composicion Menús'

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    producto = models.ForeignKey(ProductoGenerico, on_delete=models.CASCADE)
    cantidad = models.DecimalField(default=0, max_digits=8, decimal_places=4)

    def __str__(self):
        return 'Producto'


class AsignacionMenu(models.Model):
    class Meta:
        verbose_name = 'Asignación Menú'
        verbose_name_plural = 'Asignación Menús'

    punto_de_consumo = models.ForeignKey(PuntoDeConsumo, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu, blank=True)
    fecha_actualizacion = models.DateField(default=timezone.now)
    cantidad_personas = models.PositiveIntegerField(default=0)
    cantidad_dias_abierto = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.punto_de_consumo)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.fecha_actualizacion = timezone.now()
        super(AsignacionMenu, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                         update_fields=update_fields)