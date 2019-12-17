# Create your views here.

from __future__ import unicode_literals
from django.shortcuts import render
from .utileria import render_pdf, render_multiple_pdf
from django.views.generic import View
from django.http import HttpResponse
from .models import EgresosPuntoDeRecepcion, LineaDeEgr, LineaDeIng
from Organizacion.models import PuntoDeConsumo


class PDF(View):
    def get(self, request, id_context, *args, **kwargs):
        movimiento = EgresosPuntoDeRecepcion.objects.filter(id=id_context)[0]
        fecha = movimiento.fecha_y_hora_de_egreso
        origen = movimiento.origen
        destino = movimiento.destino
        pc = PuntoDeConsumo.objects.get(id=destino.id)
        lineas = LineaDeEgr.objects.filter(movimiento=id_context)
        parametros = {
            'fecha': fecha,
            'origen': origen,
            'destino': destino,
            'responsable': pc.responsable,
            'lineas': lineas
        }
        pdf = render_pdf("template_html_a_pdf.html", {"parametros": parametros})
        return HttpResponse(pdf, content_type="application/pdf")


class PDF_Multiple(View):
    def get(self, request, id_context, *args, **kwargs):
        ids = id_context.split(",")
        movimiento = EgresosPuntoDeRecepcion.objects.filter(id__in=[int(i) for i in ids])
        egresos = []
        for m in movimiento:
            fecha = m.fecha_y_hora_de_egreso
            origen = m.origen
            destino = m.destino
            pc = PuntoDeConsumo.objects.get(id=destino.id)
            lineas = LineaDeEgr.objects.filter(movimiento=m.id)
            egresos.append({'parametros': {
                'fecha': fecha,
                'origen': origen,
                'destino': destino,
                'responsable': pc.responsable,
                'lineas': lineas
            }
            })
        pdf = render_multiple_pdf("template_html_a_pdf.html", {"egresos": egresos})
        return HttpResponse(pdf, content_type="application/pdf")


class PDF_Cuadro_Fraccionamiento(View):
    def get(self, request, id_context, *args, **kwargs):
        ids = id_context.split(",")
        movimiento = EgresosPuntoDeRecepcion.objects.filter(id__in=[int(i) for i in ids])
        # genero la lista de todos los productos del ingreso y lo paso a set de tuplas para eliminar duplicados
        productos_desde_ingreso = set([(prod.producto, prod.producto_id) for prod in LineaDeIng.objects.filter(movimiento_id__in=[i.ingreso_asociado_id for i in movimiento])])

        productos = [{
                            'nombre': 'Punto de consumo',
                            'id_producto': 0
                    }] + \
                    [{
                        'nombre': str(li[0]), # la posicion 0 de la lista de tuplas es el producto
                        'id_producto': li[1] # la posicion 1 de la lista de tuplas es el id_producto
                    } for li in productos_desde_ingreso]
        pcs_con_productos = [] # el diccionario que enviare al template. se completa con los productos que tenga cada pc
        lineas_egreso = LineaDeEgr.objects.filter(movimiento__in=[m.id for m in movimiento])
        for m in movimiento: # agrego todos los productos de cada pc
            productos_pc = [] # aqui guardo todos los productos que tenga un pc
            for l in lineas_egreso:
                if m.id == l.movimiento_id:
                    productos_pc.append({'cantidad': l.cantidad, 'id_producto': l.producto_id})
            # agrego los productos que no estan para que no muestre celdas vacias
            faltantes = [{'id_producto': p['id_producto'], 'cantidad': 0} for p in productos
                         if (p['id_producto'] not in [ids['id_producto'] for ids in productos_pc] and p['id_producto'] != 0)]
            productos_pc += faltantes
            # si el punto de consumo todavia no se agrego a los puntos finales para la vista lo agrego
            if str(m.destino)[:int(str(m.destino).index('-'))] not in [pc['nombre'] for pc in pcs_con_productos]:
                pcs_con_productos.append({
                    'nombre': str(m.destino)[:int(str(m.destino).index('-'))],
                    'productos': productos_pc
                })
            else: # si ya se agrego es porque los egresos seleccionados son de mas de un ingreso y debo sumar las lineas del mismo pc que me quedan separadas
                for pc in pcs_con_productos:
                    if str(m.destino)[:int(str(m.destino).index('-'))] == pc['nombre']:
                        for x in pc['productos']:
                            for prod_pc in productos_pc:
                                if x['id_producto'] == prod_pc['id_producto']:
                                    x['cantidad'] += prod_pc['cantidad']
        parametros = {
            'cabeceras': productos,
            'pcs': pcs_con_productos
        }
        pdf = render_pdf("template_cuadro_fraccionamiento_pdf.html", {"parametros": parametros})
        return HttpResponse(pdf, content_type="application/pdf")

