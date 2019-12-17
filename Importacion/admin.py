from django.contrib import admin, messages
from .models import *
from Movimientos.models import LineaDeIng, DistribucionProducto, LineaDistribucionProducto
from Productos.models import VarianteProducto
from Organizacion.models import PuntoDeConsumo
import pandas as pd


# todo ver bien como mandar los mensajes para que sean mas claros y especificos (sobretodo los de error)
#  y hacer rollback si salta excepcion.

# Register your models here.
class ImportacionLineasIngresoAdmin(admin.ModelAdmin):
    class Meta:
        model = ImportacionLineaIngreso

    fields = ['ingreso', 'documento', 'columnas_a_importar', ]
    readonly_fields = ['columnas_a_importar']
    list_display = ['ingreso']
    actions = None

    def columnas_a_importar(self, obj):
        return 'Se importarán las columnas Producto y Cantidad.\n' \
               'El producto debe existir en las Variantes de Producto del Proveedor seleccionado en el ingreso'
    columnas_a_importar.short_description = 'Nota'

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_save_and_add_another': True,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        todo_ok = True
        try:
            excel_file = obj.documento
            lineas = pd.read_excel(excel_file)
            lineas.columns = [l.lower() for l in lineas.columns]
            ingreso = IngresosAPuntosDeRecepcion.objects.get(id=obj.ingreso_id)
            for linea in lineas.itertuples():
                nueva_linea_ing = LineaDeIng()
                nueva_linea_ing.movimiento = obj.ingreso
                nueva_linea_ing.cantidad = getattr(linea, 'cantidad')
                nueva_linea_ing.producto = VarianteProducto.objects.get(
                    denominacion__iexact=getattr(linea, 'producto'),
                    proveedor_id=ingreso.origen_id)
                nueva_linea_ing.save()
            obj.delete()

        except AttributeError:
            todo_ok = False
            mensaje = 'Falta alguna de las columnas: Producto o Cantidad en el archivo cargado'

        except ImportacionLineaIngreso.DoesNotExist and VarianteProducto.DoesNotExist:
            todo_ok = False
            mensaje = 'Alguna variante de producto no esta registrada en las Variantes de Productos del Proveedor'

        except ImportacionLineaIngreso.MultipleObjectsReturned:
            todo_ok = False
            mensaje = 'Alguna variante de producto esta registrada con el mismo nombre para un mismo proveedor'

        except ValueError:
            todo_ok = False
            mensaje = 'El documento ha sido eliminado de la base de datos, por favor carguelo nuevamente'

        finally:
            if todo_ok:
                messages.add_message(request, messages.SUCCESS, 'Se han importado las lineas de los ingresos ' +
                                     str(obj.ingreso))
            else:
                messages.set_level(request, messages.ERROR)
                messages.add_message(request, messages.ERROR, mensaje)


class ImportacionDistribucionAdmin(admin.ModelAdmin):
    class Meta:
        model = ImportacionDistribucion
    fields = ['distribucion', 'documento', 'columnas_a_importar']
    readonly_fields = ['columnas_a_importar']
    list_display = ['distribucion']
    actions = None

    def columnas_a_importar(self, obj):
        return 'Se importarán las columnas Punto de Consumo y Productos.\n' \
               'Puede haber multiples columnas de productos pero su nombre debe existir como alguna ' \
               'Variante de Producto de algun Proveedor.\nLos nombres de los puntos de consumo deben tener ' \
               'el mismo nombre con el cual estan registrados'
    columnas_a_importar.short_description = 'Nota'

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_save_and_add_another': True,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        todo_ok = True
        try:
            excel_file = obj.documento
            lineas = pd.read_excel(excel_file)
            # columnas = [columna.lower() for columna in lineas.columns]
            lineas.columns = [l.lower().strip().replace(' ', '_') for l in lineas.columns]
            lineas.drop(lineas.columns[lineas.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
            # Hago un replace porque los espacios causan errores en el getattr()
            for columna in lineas.columns:
                if not str(columna).__eq__('punto_de_consumo'):
                    nueva_distribucion_producto = DistribucionProducto()
                    nueva_distribucion_producto.distribucion = obj.distribucion
                    nueva_distribucion_producto.producto = VarianteProducto.objects.get(
                        denominacion__iexact=str(columna).replace('_', ' '))
                    nueva_distribucion_producto.save()
                    aux_ultima_linea = None
                    for linea in lineas.itertuples():
                        nueva_linea_distribucion_producto = LineaDistribucionProducto()
                        nueva_linea_distribucion_producto.distribucion = nueva_distribucion_producto
                        nueva_linea_distribucion_producto.pc = PuntoDeConsumo.objects.get(
                            nombre__icontains=str(getattr(linea, 'punto_de_consumo')))
                        nueva_linea_distribucion_producto.porcentaje = getattr(linea, str(columna))
                        nueva_linea_distribucion_producto.save()
                        aux_ultima_linea = nueva_linea_distribucion_producto
                    nueva_distribucion_producto.total_asignado = aux_ultima_linea.traerTotalAsignado()
                    nueva_distribucion_producto.save()
            obj.delete()

        except AttributeError:
            todo_ok = False
            mensaje = 'Falta columna Punto de consumo en el documento'

        except VarianteProducto.DoesNotExist:
            todo_ok = False
            mensaje = 'Alguna variante de producto no esta registrada en las Variantes de Productos o su Denominacion en ' \
                      'el documento es incorrecta'

        except ValueError:
            todo_ok = False
            mensaje = 'El documento ha sido eliminado de la base de datos, por favor carguelo nuevamente'

        finally:
            if todo_ok:
                messages.add_message(request, messages.SUCCESS, 'Se ha importado la distribucion ' +
                                     str(obj.distribucion))
            else:
                messages.set_level(request, messages.ERROR)
                messages.add_message(request, messages.ERROR, mensaje)


admin.site.register(ImportacionDistribucion, ImportacionDistribucionAdmin)
admin.site.register(ImportacionLineaIngreso, ImportacionLineasIngresoAdmin)
