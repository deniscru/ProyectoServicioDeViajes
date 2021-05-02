from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('usuario/listaUser/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuario/listaChofer/', views.listado_chofer, name='listado_chofer'),
    path('usuario/listaPersona/', views.listado_persona, name= 'listado_persona'),
    path('usuario/listaUser/', views.lisatdo_usuario, name='listado_usuario'),
    path('usuario/listaPasajero', views.lisatdo_pasajero, name='listado_pasajero'),
    path('usuario/listaCombi', views.listado_combi, name='listado_combi'),
    path('usuario/listaViaje', views.listado_viaje ,name='listado_viaje'),
    path('usuario/listaInsumo',views.listado_insumo ,name='listado_insumo'),
    path('usuario/listaRuta',views.listado_ruta ,name='listado_ruta'),
    path('usuario/listaLugar', views.listado_lugar ,name='listado_lugar'),
    path('usuario/listaTarjeta', views.listado_tarjeta ,name='listado_tarjeta'),
    path('usuario/lugarNew', views.lugar_new, name='lugar_new'),
    path('registrar/',views.pasajero_new , name='registrar'),
    path('usuario/listaPasajero/<int:pk>/', views.detalle_pasajero, name='detalle_pasajero'),
    path('usuario/listaChofer/<int:pk>/', views.detalle_chofer, name='detalle_chofer'),
    path('usuario/listaCombi/<int:pk>/', views.detalle_combi, name='detalle_combi'),
    path('usuario/listaViaje/<int:pk>/', views.detalle_viaje, name='detalle_viaje'),
    path('usuario/listaRuta/<int:pk>/', views.detalle_ruta, name='detalle_ruta'),
    path('usuario/listaTarjeta/<int:pk>/', views.detalle_tarjeta, name='detalle_tarjeta'),
    path('usuario/listaInsumo/<int:pk>/', views.detalle_insumo, name='detalle_insumo'),
    path('usuario/listaLugar/<int:pk>/', views.detalle_lugar, name='detalle_lugar'),
]
