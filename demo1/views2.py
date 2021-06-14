import json
from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import FormPasaje,FormComentario
from datetime import date, datetime,timedelta
from .models import Chofer, Pasaje,CantInsumo, Pasajero, Tarjeta, Insumo, Ruta, Viaje, Persona ,Comentario
from django.db.models import Q,F
from django.http import HttpResponse


def armarInfo(pk, estado2):
    pasajero=Persona.objects.get(usuario=pk)
    resul=Pasaje.objects.filter(activo=True, pasajero=pasajero.pk, estado=estado2).order_by('viaje__fecha')
    lista=[]
    for p in resul:
        dic={'origen': p.viaje.ruta.origen.nombre_de_lugar, 'destino': p.viaje.ruta.destino.nombre_de_lugar,
        'fecha':str(p.viaje.fecha)+', '+str(p.viaje.ruta.hora.hour)+':'+str(p.viaje.ruta.hora.minute), 'costoTotal':p.costoTotal, 
        'pk':p.pk, 'cantidad':p.cantidad}
        if estado2=="CANCELADO":
            dic['costoDevuelto']=p.costoDevuelto
        lista.append(dic)
    return lista

def consultarPasajesUserPendi(request, pk):
    lista=armarInfo(pk, "PENDIENTE")
    return render(request, 'demo1/listados/lisPasajesPendien.html', {'lista':lista, 'valor': True if len(lista)!=0 else False})  

def consultarPasajesUserCance(request, pk):
    lista=armarInfo(pk, "CANCELADO")
    return render(request, 'demo1/listados/lisPasajesCance.html', {'lista':lista, 'valor': True if len(lista)!=0 else False})

def es_antes_48(viaje):
    fecha_viaje=viaje.fecha
    ruta=Ruta.objects.get(id=viaje.ruta_id)
    hora_ruta=ruta.hora
    hora_dia_actual=datetime.now()
    hora_dia_actual=datetime(hora_dia_actual.year,hora_dia_actual.month,hora_dia_actual.day,hora_dia_actual.hour,hora_dia_actual.minute)
    hora_dia_viaje=datetime(fecha_viaje.year,fecha_viaje.month,fecha_viaje.day,hora_ruta.hour,hora_ruta.minute)
    diferencia=hora_dia_viaje - hora_dia_actual
    return diferencia

def cancelar_pasaje(request,pk):
    cancelado_48=False
    cancelado_dentro=False
    pasado=False
    Pasaje.objects.filter(id=pk,estado="PENDIENTE").update(estado="CANCELADO")
    pasaje=Pasaje.objects.get(id=pk)
    Viaje.objects.filter(id=pasaje.viaje_id).update(asientos=F("asientos")+pasaje.cantidad)
    Viaje.objects.filter(id=pasaje.viaje_id).update(vendidos=F("vendidos") - pasaje.cantidad)
    viaje=Viaje.objects.get(id=pasaje.viaje_id)
    diferencia=es_antes_48(viaje)
    if diferencia>=timedelta(hours=48):
        Pasaje.objects.filter(id=pk).update(costoDevuelto=F("costoTotal"))
        cancelado_48=True
    elif diferencia<timedelta(hours=48) and diferencia >timedelta(minutes=1):
        Pasaje.objects.filter(id=pk).update(costoDevuelto=F("costoTotal")/2)
        cancelado_dentro=True
    else:
        pasado=True
    lista=armarInfo(request.user.id,"PENDIENTE")
    return render(request, 'demo1/listados/lisPasajesPendien.html', {'lista':lista, 'valor': True if len(lista)!=0 else False, "cancelado_48":cancelado_48,"cancelado_dentro":cancelado_dentro,"pasado":pasado})

def armar_texto(texto):
    string=""
    cantidad=0
    for i in texto:
        cantidad+=1
        if cantidad <115:
            string=string+i
        else:
            string=string+"\n"+i
            cantidad=0
    return string

def modificar_comentario(request,pk):
    comentario=Comentario.objects.get(pk=pk)
    exitoso=False
    fallido=False
    if request.method=="POST":
        form=FormComentario(request.POST)
        if form.is_valid():
            datos=form.cleaned_data
            if len (datos["texto"])>115:
                    texto=armar_texto(datos["texto"])
            else:
                texto=datos["texto"]
            if comentario.texto != texto:
                Comentario.objects.filter(id=pk).update(texto=texto,fecha=date.today(),hora=datetime.now().time())
                exitoso=True
            else:
                fallido=True
    else:
        data={'texto':comentario.texto}
        form=FormComentario(data)
    return render(request,'demo1/modificar/formulario_modificar_comentario.html', {'form': form,"exitoso":exitoso,"fallido":fallido})

def armarDatosDePrecio():
    insumos=Insumo.objects.filter(activo=True)
    lista=[]
    for i in insumos:
        dic={}
        dic['id']=i.pk
        dic['precio']=i.precio
        lista.append(dic)
    return lista

def registrarPasaje(insumos, cantInsumos, total, cantAsientos, unPasajero, unViaje):
    pasaje= Pasaje.objects.create(pasajero=unPasajero, viaje=unViaje, costoTotal=total, cantidad=cantAsientos, estado="PENDIENTE")
    unViaje.asientos=unViaje.asientos-cantAsientos
    unViaje.save()
    for i in range(len(insumos)):
        unInsumo=Insumo.objects.get(id=int(insumos[i]))
        unCantInsumo=CantInsumo.objects.create(insumo=unInsumo, cantidad=int(cantInsumos[i]))
        pasaje.cantInsumos.add(unCantInsumo)

def prueba(request, pk=None, *arg, **kwags):
    pasajero=Pasajero.objects.get(usuario=request.user.pk)
    esGold= True if pasajero.tipo=='GOLD' else False
    if esGold:
        miTarjeta=Tarjeta.objects.get(pasajero=pasajero)
    else:
        miTarjeta=None
    viaje=Viaje.objects.get(id=pk)
    precios= armarDatosDePrecio()
    if request.is_ajax():
        form=FormPasaje(request.POST)
        insumos=request.GET.getlist('dato[]')
        cantInsumos=request.GET.getlist('datos[]')
        total=request.GET.get('total')
        cantAsientos=request.GET.get('cant')
        registrarPasaje(insumos, cantInsumos, float(total), int(cantAsientos), pasajero, viaje)
        user=User.objects.get(id=request.user.pk)
        fecha=str(date.today())
        hora=datetime.today().ctime().split()
        datosAEnviar=[{"nombre":user.first_name+" "+user.last_name,"costo":234, "total":total,
                        "origen":viaje.ruta.origen.__str__(), "destino":viaje.ruta.destino.__str__(),
                        "cant":cantAsientos, "fecha":fecha, "hora":hora[3]}]
        dato=json.dumps(datosAEnviar)
        return HttpResponse(dato, 'application/json')
    else:
        if request.method== 'POST':
            form=FormPasaje(request.POST)
        else:
            form= FormPasaje()
        return render(request, 'demo1/form/formulario_prueba.html', {'form':form, 'esGold':esGold, 'pk':pk, 'conPrecios':precios, 'precioDeViaje':viaje.precio, 'miTarjeta':miTarjeta, "cantAsientos":viaje.asientos})
