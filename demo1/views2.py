from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import FormLugar,FormPasaje, FormCambiarContraseña,FormPasajeroModi, FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormTarjeta, FormoBusquedaViaje
from datetime import date, datetime,timedelta
from django.core.paginator import Paginator
from .models import Chofer, Pasaje,CantInsumo, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona
from django.contrib.auth.hashers import make_password
from django.db.models import Q,F
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView,View

dicPasajeros={}


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

class InicializarPasaje(TemplateView):
    template_name = 'sumar_al_pasaje'
    def get(self,request,pk,*args,**kwargs):
        dicPasajeros[buscar_pasajero(request.user.pk).id]=[{},{}]
        return redirect(self.template_name,pk)

def obtener_tarjeta(pk):
    queryset=Tarjeta.objects.filter(activo=True)
    for tarjeta in queryset:
        if tarjeta.pasajero.id == pk:
            return tarjeta

def sumar_al_pasaje(request,pk):
    gold=False
    descuento=0
    compro=False
    cantInsumos=dicPasajeros[buscar_pasajero(request.user.pk).id][1]
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
                    dicPasajeros[buscar_pasajero(request.user.pk).id][1]=cantInsumos
                if gold:
                    descuento=round((pasaje['precio'] * 0.1),2)
                    pasaje['precio']-=descuento
                pasaje['pasajero']=pasajero
                pasaje['viaje']=viaje
                pasaje['cantInsumos']=cantInsumos
                pasaje['numero']=p['numero']
                pasaje['codigo']=p['codigo']
                pasaje['fecha_de_vencimiento']=p['fecha_de_vencimiento']
                dicPasajeros[buscar_pasajero(request.user.pk).id][0]=pasaje
                
    else:
        form = FormPasaje()
    return render(request, 'demo1/sumar_al_pasaje.html', {'form': form,'hayPasajes':hayPasajes,'viaje':viaje,'cantInsumos':cantInsumos,'pasaje':pasaje,'hayPasajesSelec':hayPasajesSelec,'hayInsumosSelec':hayInsumosSelec,'compro':compro,'gold':gold,'descuento':descuento})


def cargar_datos_de_tarjeta(request,pk):
    gold=False
    compro=False
    descuento=0
    cantInsumos=dicPasajeros[buscar_pasajero(request.user.pk).id][1]
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
                    dicPasajeros[buscar_pasajero(request.user.pk).id][1]=cantInsumos
                if gold:
                    descuento=round((pasaje['precio'] * 0.1),2)
                    pasaje['precio']-=descuento
                pasaje['pasajero']=pasajero
                pasaje['viaje']=viaje
                pasaje['cantInsumos']=cantInsumos
                pasaje['numero']=p['numero']
                pasaje['codigo']=p['codigo']
                pasaje['fecha_de_vencimiento']=p['fecha_de_vencimiento']
                dicPasajeros[buscar_pasajero(request.user.pk).id][0]=pasaje
         
                    

    else:
        tarj=obtener_tarjeta(pasajero.pk)
        data={'cantidad':'1','numero':tarj.numero,'fecha_de_vencimiento':tarj.fecha_de_vencimiento,'codigo':tarj.codigo}
        form = FormPasaje(data)
    return render(request, 'demo1/sumar_al_pasaje.html', {'form': form,'hayPasajes':hayPasajes,'viaje':viaje,'cantInsumos':cantInsumos,'pasaje':pasaje,'hayPasajesSelec':hayPasajesSelec,'hayInsumosSelec':hayInsumosSelec,'compro':compro,'gold':gold,'descuento':descuento})

def validando(request):
    return render(request, 'demo1/validando.html')


def validar_compra(request):
    ok=True
    pasaj=None
    error=''
    pasaje=dicPasajeros[buscar_pasajero(request.user.pk).id][0]
    #pasaje=FormPasaje().get_pasaje()
    if pasaje['pasajero'].tipo == 'GOLD':
        gold=True
    else:
        gold=False
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
        dicPasajeros[buscar_pasajero(request.user.pk).id]=[{},{}]
        #c={}
        #p={}
        #FormPasaje().change_cantInsumos(c)
        #FormPasaje().change_pasaje(p)
    return render(request, 'demo1/validar_compra.html', {'gold':gold,'ok': ok,'error':error,'pasaje':pasaje,'pk':pasaje['viaje'].id,'nombre':pasaje['pasajero'].usuario.first_name,'apellido':pasaje['pasajero'].usuario.last_name,'costo':pasaje['precio'],'origen':pasaje['viaje'].ruta.origen.nombre_de_lugar,'destino':pasaje['viaje'].ruta.destino.nombre_de_lugar,'fecha':pasaje['viaje'].fecha,'hora':pasaje['viaje'].ruta.hora,'asientos':pasaje['cantidad'],'insumos':pasaje['cantInsumos']})


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
    pasajero=Persona.objects.get(usuario=pk)
    resul=Pasaje.objects.filter(activo=True, pasajero=pasajero.pk, estado=estado2).order_by('viaje__fecha')
    lista=[]
    for p in resul:
        dic={'origen': p.viaje.ruta.origen.nombre_de_lugar, 'destino': p.viaje.ruta.destino.nombre_de_lugar,
        'fecha':str(p.viaje.fecha)+', '+str(p.viaje.ruta.hora.hour)+':'+str(p.viaje.ruta.hora.minute), 'costoTotal':p.costoTotal, 'pk':p.pk}
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

def cambiar_a_cancelado(pk):
    Pasaje.objects.filter(id=pk,estado="PENDIENTE").update(estado="CANCELADO")
    pasaje=Pasaje.objects.get(id=pk)
    Viaje.objects.filter(id=pasaje.viaje_id).update(asientos=F("asientos")+1)
    viaje=Viaje.objects.get(id=pasaje.viaje_id)
    diferencia=es_antes_48(viaje)
    if diferencia>=timedelta(hours=48):
        pasaje.objects.filter(id=pk).update(costoDevuelto=F("costoTotal"))
    elif diferencia<timedelta(hours=48) and diferencia >timedelta(minutes=1):
        pasaje.objects.filter(id=pk).update(costoDevuelto=F("costoTotal")/2)

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
