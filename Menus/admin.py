from django.contrib import admin
from .models import *


class ComposicionInLine(admin.TabularInline):
    class Meta:
        model = ComposicionMenu
    model = ComposicionMenu


class MenuAdmin(admin.ModelAdmin):
    class Meta:
        model = Menu
    model = Menu
    # Agregar resource
    inlines = [ComposicionInLine]
    list_display = ['denominacion', 'prioridad', 'fecha_actualizacion']
    readonly_fields = ['fecha_actualizacion']


class AsignacionAdmin(admin.ModelAdmin):
    class Meta:
        model = AsignacionMenu
    model = AsignacionMenu
    fields = ['punto_de_consumo', 'fecha_actualizacion', 'cantidad_personas', 'cantidad_dias_abierto', 'menu']
    filter_horizontal = ('menu',)
    list_display = ['punto_de_consumo', 'cantidad_personas', 'cantidad_dias_abierto', 'fecha_actualizacion']
    readonly_fields = ['fecha_actualizacion']


# admin.site.register(Menu, MenuAdmin)
# admin.site.register(AsignacionMenu, AsignacionAdmin)