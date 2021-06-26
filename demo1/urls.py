from django.urls import path
from django.conf.urls import url
from . import views
from . import views2

urlpatterns = [
    path('', views.principal, name='principal'),
    path('usuario/listaUser/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuario/listaChofer/', views.listado_chofer, name='listado_chofer'),
    path('usuario/listaCombi', views.listado_combi, name='listado_combi'),
    path('usuario/listaViaje', views.listado_viaje ,name='listado_viaje'),
    path('usuario/listaInsumo',views.listado_insumo ,name='listado_insumo'),
    path('usuario/listaRuta',views.listado_ruta ,name='listado_ruta'),
    path('usuario/listaLugar', views.listado_lugar ,name='listado_lugar'),
    path('usuario/lugarNew', views.lugar_new, name='lugar_new'),
    path('usuario/choferNew', views.chofer_new, name='chofer_new'),
    path('usuario/combiNew', views.combi_new, name='combi_new'),
    path('usuario/viajeNew', views.viaje_new, name='viaje_new'),
    path('usuario/insumoNew', views.insumo_new, name='insumo_new'),
    path('usuario/rutaNew', views.ruta_new, name= 'ruta_new'),
    path('registrar/',views.pasajero_new , name='registrar'),
    path('usuario/listaChofer/<int:pk>/', views.detalle_chofer, name='detalle_chofer'),
    path('usuario/listaCombi/<int:pk>/', views.detalle_combi, name='detalle_combi'),
    path('usuario/listaTarjeta/<int:pk>/', views.detalle_tarjeta, name='detalle_tarjeta'),
    path('usuario/listaLugar/<int:pk>/', views.detalle_lugar, name='detalle_lugar'),
    path('usuario/listaLugar/modificar/<int:pk>/', views.modificar_lugar, name='modificar_lugar'),
    path('usuario/listaInsumo/modificar/<int:pk>/', views.modificar_insumo, name='modificar_insumo'),
    path('usuario/listaRuta/modificar/<int:pk>/', views.modificar_ruta, name='modificar_ruta'),
    path('usuario/listaChofer/modificar/<int:pk>/', views.modificar_chofer, name='modificar_chofer'),
    path('usuario/listaCombi/modificar/<int:pk>/', views.modificar_combi, name='modificar_combi'),
    path('usuario/listaViaje/modificar/<int:pk>/', views.modificar_viaje, name='modificar_viaje'),
    path('usuario/listaLugar/eliminar/<int:pk>/', views.eliminar_lugar, name='eliminar_lugar'),
    path('usuario/listaChofer/eliminar/<int:pk>/', views.eliminar_chofer, name='eliminar_chofer'),
    path('usuario/listaCombi/eliminar/<int:pk>/', views.eliminar_combi, name='eliminar_combi'),
    path('usuario/listaViaje/eliminar/<int:pk>/', views.eliminar_viaje, name='eliminar_viaje'),
    path('usuario/listaInsumo/eliminar/<int:pk>/', views.eliminar_insumo, name='eliminar_insumo'),
    path('usuario/listaRuta/eliminar/<int:pk>/', views.eliminar_ruta, name='eliminar_ruta'),
    path('login/',views.login_usuario,name='login'),
    path('registrar/registrar_tarjeta/<int:pk>/',views.tarjeta_new,name="registrar_tarjeta"),
    path('registrar_tarjeta_modificado/<int:pk>/',views.tarjeta_new_modificado,name="registrar_tarjeta_modificado"),
    path('home_usuario/',views.home_usuario,name="home_usuario"),
    path('home_usuario/<int:pk>/',views.home_usuario,name="home_usuario"),
    path('home_usuario/modificar_pasajero/<int:pk>/',views.modificar_pasajero,name="modificar_pasajero"),
    path('home_usuario_chofer/',views.home_usuario_chofer,name="home_usuario_chofer"),
    path('logout/',views.logout_usuario,name='logout'),
    path('home_usuario/buscar_viaje',views.buscarViajes,name="buscar_viajes"),
    path('home_usuario/crear_comentario/',views.comentario_new,name="crear_comentario"),
    path('home_usuario/consultarPasajes1/<int:pk>',views2.consultarPasajesUserPendi,name="consultar_pasaje_user_p"),
    path('home_usuario/consultarPasajes2/<int:pk>',views2.consultarPasajesUserCance,name="consultar_pasaje_user_c"),
    path('home_usuario/consultarPasajes1/cancelar/<int:pk>',views2.cancelar_pasaje,name="cancelar_pasaje"),
    path('home_usuario/modificar/<int:pk>',views2.modificar_comentario,name="modificar_comentario"),
    path('home_usuario/buscar_viaje/comprar_pasaje/<int:pk>',views2.prueba,name="comprar_pasaje_form"),
    path('change_password/<int:pk>', views2.change_password, name='change_password'),
    path('iniciarViaje/<int:pk>', views2.iniciarViaje, name='iniciar_viaje'),
    path('finalizarViaje', views2.finalizarViaje, name='finalizar_viaje'),
    path('registrarSintomas/<int:pk>', views2.registrarSintomas, name='registrar_sintomas'),
    path("home_usuario_chofer/viajes_proximos", views2.viajes_proximos, name="viajes_proximos"),
    path("home_usuario_chofer/viajes_proximos/listado_pasajeros/<int:pk>", views2.pasajeros_de_viajes_proximos, name="pasajeros_viajes_proximos"),
]
