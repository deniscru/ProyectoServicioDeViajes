from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import FormLugar,FormPasaje, FormCambiarContraseña,FormPasajeroModi, FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormTarjeta, FormoBusquedaViaje
from datetime import date, datetime
from django.core.paginator import Paginator
from .models import Chofer, Pasaje,CantInsumo, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



def change_password(request,pk):
    exito=False
    user=request.user
    if request.method == 'POST':
        form = FormCambiarContraseña(request.POST)
        if form.is_valid():
            c=form.cleaned_data
            user.password=make_password(c['password'])
            user.save()
            login(request, user)
            exito=True
        return render(request, 'demo1/change_password.html', {'form': form,'exito':exito,'user':user})
    else:
        form = FormCambiarContraseña()
    return render(request, 'demo1/change_password.html', {'form': form,'exito':exito,'user':user})

def buscar_pasajero(pk):
    queryset=Pasajero.objects.filter(activo=True)
    for pasajero in queryset:
        if pasajero.usuario.id == pk:
            return pasajero

def inicializar_pasaje(request,pk):
    cantInsumos={}
    pasaje={}
    FormPasaje().change_cantInsumos(cantInsumos)
    FormPasaje().change_pasaje(pasaje)
    return redirect('sumar_al_pasaje',pk)


def obtener_tarjeta(pk):
    queryset=Tarjeta.objects.filter(activo=True)
    for tarjeta in queryset:
        if tarjeta.pasajero.id == pk:
            return tarjeta

def sumar_al_pasaje(request,pk):
    gold=False
    descuento=0
    compro=False
    cantInsumos=FormPasaje().get_cantInsumos()
    pasaje={}
    pasajero = buscar_pasajero(request.user.pk)
    if pasajero.tipo=='GOLD':
        gold=True
    viaje= Viaje.objects.get(pk=pk)
    hayPasajes=True
    hayPasajesSelec=False
    hayInsumosSelec=False
    if request.method == 'POST':
        form = FormPasaje(request.POST)
        if form.is_valid():
            p=form.cleaned_data
            hayPasajes= viaje.asientos >= int(p['cantidad']) and int(p['cantidad']) > 0
            if hayPasajes:
                pasaje['precio']=viaje.precio * p['cantidad']
                compro=True
                hayPasajesSelec=True
                pasaje['cantidad']=p['cantidad']
                try:
                    if int(p['cantInsumo']) > 0:
                        cantInsumos[str(p['insumos'].nombre)]= p['cantInsumo']
                    else:
                        try:
                            del cantInsumos[str(p['insumos'].nombre)]
                        except:
                            pass
                except:
                    pass                    
                if cantInsumos != {}:
                    hayInsumosSelec=True
                    for key in cantInsumos:
                        pasaje['precio']=pasaje['precio'] + (Insumo.objects.filter(nombre=key)[0].precio * cantInsumos[key])
                    FormPasaje().change_cantInsumos(cantInsumos)
                if gold:
                    descuento=round((pasaje['precio'] * 0.1),2)
                    pasaje['precio']-=descuento
                pasaje['pasajero']=pasajero
                pasaje['viaje']=viaje
                pasaje['cantInsumos']=cantInsumos
                pasaje['numero']=p['numero']
                pasaje['codigo']=p['codigo']
                pasaje['fecha_de_vencimiento']=p['fecha_de_vencimiento']
                FormPasaje().change_pasaje(pasaje)

    else:
        form = FormPasaje()
    return render(request, 'demo1/sumar_al_pasaje.html', {'form': form,'hayPasajes':hayPasajes,'viaje':viaje,'cantInsumos':cantInsumos,'pasaje':pasaje,'hayPasajesSelec':hayPasajesSelec,'hayInsumosSelec':hayInsumosSelec,'compro':compro,'gold':gold,'descuento':descuento})

def cargar_datos_de_tarjeta(request,pk):
    gold=False
    compro=False
    descuento=0
    cantInsumos=FormPasaje().get_cantInsumos()
    pasaje={}
    pasajero = buscar_pasajero(request.user.pk)
    if pasajero.tipo=='GOLD':
        gold=True
    viaje= Viaje.objects.get(pk=pk)
    hayPasajes=True
    hayPasajesSelec=False
    hayInsumosSelec=False
    if request.method == 'POST':
        form = FormPasaje(request.POST)
        if form.is_valid():
            p=form.cleaned_data
            hayPasajes= viaje.asientos >= p['cantidad']
            if hayPasajes:
                pasaje['precio']=viaje.precio * p['cantidad']
                compro=True
                hayPasajesSelec=True
                pasaje['cantidad']=p['cantidad']
                try:
                    if int(p['cantInsumo']) > 0:
                        cantInsumos[str(p['insumos'].nombre)]= p['cantInsumo']
                    else:
                        try:
                            del cantInsumos[str(p['insumos'].nombre)]
                        except:
                            pass
                except:
                    pass                    
                if cantInsumos != {}:
                    hayInsumosSelec=True
                    for key in cantInsumos:
                        pasaje['precio']=pasaje['precio'] + (Insumo.objects.filter(nombre=key)[0].precio * cantInsumos[key])
                    FormPasaje().change_cantInsumos(cantInsumos)
                if gold:
                    descuento=round((pasaje['precio'] * 0.1),2)
                    pasaje['precio']-=descuento
                pasaje['pasajero']=pasajero
                pasaje['viaje']=viaje
                pasaje['cantInsumos']=cantInsumos
                pasaje['numero']=p['numero']
                pasaje['codigo']=p['codigo']
                pasaje['fecha_de_vencimiento']=p['fecha_de_vencimiento']
                FormPasaje().change_pasaje(pasaje)
                    

    else:
        tarj=obtener_tarjeta(pasajero.pk)
        data={'cantidad':'1','numero':tarj.numero,'fecha_de_vencimiento':tarj.fecha_de_vencimiento,'codigo':tarj.codigo}
        form = FormPasaje(data)
    return render(request, 'demo1/sumar_al_pasaje.html', {'form': form,'hayPasajes':hayPasajes,'viaje':viaje,'cantInsumos':cantInsumos,'pasaje':pasaje,'hayPasajesSelec':hayPasajesSelec,'hayInsumosSelec':hayInsumosSelec,'compro':compro,'gold':gold,'descuento':descuento})


def validar_compra(request):
    ok=True
    pasaj=None
    error=''
    pasaje=FormPasaje().get_pasaje()
    if tarjetaRepetida(pasaje['numero']):
        tarj=Tarjeta.objects.get(numero=(pasaje['numero']))
        if tarj.pasajero.pk == pasaje['pasajero'].pk:
            if tarj.fecha_de_vencimiento == pasaje['fecha_de_vencimiento']:
                if tarj.codigo == pasaje['codigo']:
                    pass
                else:
                    ok=False
                    error='El codigo de Seguridad no pertenece a la tarjeta ingresada'
            else:
                ok=False
                error='La fecha de vencimiento no corresponde con el numero de tarjeta ingresada'
        else:
            ok=False
            error='La tarjeta pertenece a otra persona no se realizo la compra'
    else:
        if fecha_vencimiento_es_valida(pasaje['fecha_de_vencimiento']):
            if pasaje['codigo'] > 99 and pasaje['codigo'] < 1000:
                pass
            else:
                ok=False
                error='El codigo ingresado no es valido'
        else:
            ok=False
            error='El vencimiento ingresado no es valido'
    if ok:
        sumar_insumos(pasaje['viaje'],pasaje['cantInsumos'])
        pasaje['viaje'].asientos = pasaje['viaje'].asientos - pasaje['cantidad']
        pasaje['viaje'].vendidos = pasaje['viaje'].vendidos + pasaje['cantidad']
        pasaje['viaje'].save()
        pasaj = Pasaje.objects.create(estado='PENDIENTE',pasajero=(pasaje['pasajero']),viaje=(pasaje['viaje']),cantidad=(pasaje['cantidad']),costoTotal=(pasaje['precio']))
        if pasaje['cantInsumos'] != {}:
            for key in pasaje['cantInsumos']:
                insumo_in=Insumo.objects.get(nombre=key)
                cantInsumo=CantInsumo.objects.create(insumo=insumo_in,cantidad=pasaje['cantInsumos'][key])
                pasaje['viaje'].cantInsumos.add(cantInsumo)
        pasaj.save()
        c={}
        p={}
        FormPasaje().change_cantInsumos(c)
        FormPasaje().change_pasaje(p)
    return render(request, 'demo1/validar_compra.html', {'ok': ok,'error':error,'pasaje':pasaje,'pasaj':pasaj})

def sumar_insumos(viaje,cantInsumos):
    if cantInsumos != {}:
        encontrado=False
        for key in cantInsumos:
            encontrado=False
            try:
                for i in viaje.cantInsumos.filter(activo=True):
                    if i.insumo.nombre == key:
                       i.cantidad= i.cantidad + cantInsumos[key]
                       
                       encontrado=True
                       break
            except viaje.DoesNotExist:
                pass
            if not encontrado:
                insumo_in=Insumo.objects.get(nombre=key)
                cantInsumo=CantInsumo.objects.create(insumo=insumo_in,cantidad=cantInsumos[key])
                viaje.cantInsumos.add(cantInsumo)
                
        viaje.save()
        return True
    else:
        return False


def tarjetaRepetidaModificado(pk,numero):
    return Tarjeta.objects.exclude(pk=pk).filter(activo=True).filter(numero=numero).exists()

def tarjetaRepetida(numero):
    return Tarjeta.objects.filter(activo=True).filter(numero=numero).exists()

def fecha_vencimiento_es_valida(fecha_de_vencimiento):
    hoy=date.today()
    return fecha_de_vencimiento > hoy

def tiene_tarjeta(pk):
    queryset=Tarjeta.objects.filter(activo=True)
    for tarjeta in queryset:
        if tarjeta.pasajero.id == pk:
            return True
    return False

def obtener_tarjeta(pk):
    queryset=Tarjeta.objects.filter(activo=True)
    for tarjeta in queryset:
        if tarjeta.pasajero.id == pk:
            return tarjeta

def armarInfo(pk, estado2):
    resul=Pasaje.objects.filter(activo=True, pasajero=pk, estado=estado2)
    lista=[]
    for p in resul:
        dic={'origen': p.viaje.ruta.origen.nombre_de_lugar, 'destino': p.viaje.ruta.destino.nombre_de_lugar,
        'fecha':p.viaje.fecha, 'costoTotal':p.costoTotal, 'pk':p.pk}
        if estado2=="CANCELADO":
            dic['costoDevuelto']=p.costoDevuelto
        lista.append(dic)
    return lista

def consultarPasajesUserPendi(request, pk):
    lista=armarInfo(pk, "PENDIENTE")
    return render(request, 'demo1/listados/lisPasajespendien.html', {'lista':lista, 'valor': True if len(lista)!=0 else False})  

def consultarPasajesUserCance(request, pk):
    lista=armarInfo(pk, "CANCELADO")
    return render(request, 'demo1/listados/lisPasajesCance.html', {'lista':lista, 'valor': True if len(lista)!=0 else False})
