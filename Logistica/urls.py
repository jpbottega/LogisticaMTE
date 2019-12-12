"""Logistica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from Movimientos.views import *
#from Stock.views import *
from django.conf import settings
from django.conf.urls.static import static

#, includes
#path('admin/', include('material.admin.urls')),

urlpatterns = [
    path('', admin.site.urls),
    path('remito/<int:id_context>/', PDF.as_view(), name="REMITO"),
    # path('stock', Stock.as_view() ,name="Stock")
    path('remito/remitos_en_masa/<str:id_context>', PDF_Multiple.as_view(), name="Remito_en_masa"),
    path('cuadro_fraccionamiento/<str:id_context>', PDF_Cuadro_Fraccionamiento.as_view(), name="Cuadro_Fraccionamiento"),

]

# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Logística MTE - CTEP'
