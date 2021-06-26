import json
from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import FormPasaje,FormComentario, FormCambiarContraseña, RegistroSintomas
from datetime import date, datetime,timedelta,time
from .models import Chofer, Pasaje,CantInsumo, Pasajero, Tarjeta, Insumo, Ruta, Viaje, Persona ,Comentario
from django.db.models import Q,F
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login

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

def registrar_ausencia(request,pk):
    pasaje=Pasaje.objects.get(id=pk)
    if (pasaje.viaje.fecha == date.today() and pasaje.viaje.ruta.hora < datetime.now().time()):
        Pasaje.objects.filter(id=pk).update(estado="CANCELADO")
        Viaje.objects.filter(id=pasaje.viaje_id).update(asientos=F("asientos")+pasaje.cantidad)
        Viaje.objects.filter(id=pasaje.viaje_id).update(vendidos=F("vendidos") - pasaje.cantidad)
        Pasaje.objects.filter(id=pk).update(costoDevuelto=0)
    lista= Pasaje.objects.filter(activo=True,estado="PENDIENTE", viaje_id=pk)
    return render(request, "demo1/listados/pasajeros_viajes_proximos.html",{'lista':lista, 'valor': True if len(lista)!=0 else False})


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
        dic['nombre']=i.nombre
        lista.append(dic)
    return lista

def registrarPasaje(insumos, cantInsumos, total, cantAsientos, unPasajero, unViaje):
    pasaje= Pasaje.objects.create(pasajero=unPasajero, viaje=unViaje, costoTotal=total, cantidad=cantAsientos, estado="PENDIENTE")
    unViaje.asientos=unViaje.asientos-cantAsientos
    unViaje.vendidos=unViaje.vendidos + cantAsientos
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

def buscar_chofer(pk):
    queryset=Chofer.objects.filter(activo=True)
    for chofer in queryset:
        if chofer.usuario.id == pk:
            return chofer

def viajesEnCurso(chofer):
    viajes=Viaje.objects.filter(activo=True).filter(estado='ENCURSO')
    if viajes.exists():
        for viaje in viajes:
            if viaje.ruta.combi.chofer.id ==chofer.id:
                return True
    return False

def viajesEnCursoId(chofer):
    viajes=Viaje.objects.filter(activo=True).filter(estado='ENCURSO')
    for viaje in viajes:
        if viaje.ruta.combi.chofer.id ==chofer.id:
            return viaje
    

def iniciarViaje(request,pk):
    enCurso=False
    ok=True
    mensaje=''
    chofer=buscar_chofer(request.user.pk)
    viaje=Viaje.objects.get(pk=pk)
    if not (viaje.fecha == date.today() and viaje.ruta.hora < datetime.now().time()):
        ok=False #ya debe haberse verificado que el viaje pertenzca al chofer y que este en estado pendiente al ingresar al listado
        mensaje='el viaje seleccionado no pertenece a los viajes del dia de hoy o la hora de inicio todavia no llego'
    if Pasaje.objects.filter(activo=True).filter(viaje=viaje).filter(estado="PENDIENTE").exists():
        ok=False
        mensaje="No puede iniciar el viaje porque hay pasajeros que no fueron revisados"
    if ok:
        pasajes=Pasaje.objects.filter(activo=True).filter(viaje=viaje).filter(estado="ACEPTADO")
        if pasajes.exists():
            for pasaje in pasajes:
                pasaje.estado='ENCURSO'
                pasaje.save()
            viaje.estado='ENCURSO'
            viaje.save()
            mensaje='El viaje fue iniciado correctamente'
        else:
            ok=False
            mensaje="no se puede iniciar el viaje porque no hay pasajeros para iniciarlo"
        
    lista_viajes_proximos=armarInfo2(request.user.pk)
    return render(request, "demo1/listados/viajes_proximos.html",{'lista':lista_viajes_proximos, 'valor': True if len(lista_viajes_proximos)!=0 else False,"mensaje":mensaje})
    

def finalizarViaje(request):
    enCurso=False
    ok=True
    mensaje=''
    chofer=buscar_chofer(request.user.pk)
    if ok:
        viaje = viajesEnCursoId(chofer)
        viaje.estado='PASADO'
        viaje.save()
        mensaje='El viaje fue finalizado correctamente'
        pasajes=Pasaje.objects.filter(activo=True).filter(viaje=viaje).filter(estado="ACEPTADO")
        if pasajes.exists():
            for pasaje in pasajes:
                pasaje.estado='PASADO'
                pasaje.save()
    return render(request, "demo1/home_usuario_chofer.html", {"enCurso":enCurso,"mensaje":mensaje}) 

def registrarSintomas(request,pk):
    ok=False
    mensaje="No puede registrar los sintomas de este pasajero porque no esta pendiente de registracion"
    pasaje=Pasaje.objects.get(pk=pk)
    viajeId=pasaje.viaje.pk
    pasajero=pasaje.pasajero
    if pasaje.estado=="PENDIENTE":
        if (pasaje.viaje.fecha == date.today() and pasaje.viaje.ruta.hora < datetime.now().time()):
            ok=True
            mensaje=""
        else:
            ok=False
            mensaje="No puede registrar los sintomas de este pasajero porque no llego el dia o la hora del viaje"

    if request.method=="POST":
        form=RegistroSintomas(request.POST)
        if form.is_valid():
            datos=form.cleaned_data
            temp=datos["temp"]
            if temp >= 38:
                ok=False
                mensaje="El pasajero presenta mas de 38 grados por tanto no puede abordar la unidad"
            if ok:
                cant=0
                if int(datos["tos"])==1:
                    cant+=1
                if int(datos["dolor_de_cabeza"])==1:
                    cant+=1
                if int(datos["falta_de_aire"])==1:
                    cant+=1
                if int(datos["diarrea"])==1:
                    cant+=1
                if int(datos["dolor_de_garganta"])==1:
                    cant+=1
                if int(datos["perdida_del_gusto"])==1:
                    cant+=1
                if int(datos["perdida_de_olfato"])==1:
                    cant+=1
                if int(datos["dolor_en_el_pecho"])==1:
                    cant+=1
                print(cant)
                if cant > 1:
                    ok=False
                    mensaje="El pasajero presenta mas 2 o mas sintomas de covid19 y no puede abordar la unidad"
            if not ok:
                pasaje.estado="RECHAZADO"
                pasaje.costoDevuelto=pasaje.costoTotal
                pasajero.habilitado=False
                pasajero.fecha_habilitacion=date.today() + timedelta(days=14)
                
            else:
                pasaje.estado="ACEPTADO"
                pasajero.habilitado=True
                pasajero.fecha_habilitacion=date.today()
                mensaje="El pasajero fue aceptado para abordar la unidad"
            pasajero.save()
            pasaje.save()

    else:
        form=RegistroSintomas()
    return render(request, "demo1/registrarSintomas.html", {"form":form,"viajeId":viajeId,"mensaje":mensaje})

def armarInfo2(pk):
    chofer=Persona.objects.get(usuario=pk)
    viajes_pendientes=Viaje.objects.filter(activo=True, estado="PENDIENTE")
    lista=[]
    for p in viajes_pendientes:
        if p.ruta.combi.chofer.id == chofer.id:
            pasajes=Pasaje.objects.filter(activo=True,estado="PENDIENTE", viaje=p)
            cantidad=0
            if len(pasajes)!=0:
                for i in pasajes:
                    cantidad=cantidad+i.cantidad
            dic={'origen': p.ruta.origen.nombre_de_lugar, 'destino': p.ruta.destino.nombre_de_lugar,
            'fecha':str(p.fecha)+', '+str(p.ruta.hora.hour)+':'+str(p.ruta.hora.minute), "cantidad":cantidad, "combi":p.ruta.combi, "pk":p.pk}
            lista.append(dic)
    return lista

def viajes_proximos(request):
    mensaje=''
    lista_viajes_proximos=armarInfo2(request.user.pk)
    return render(request, "demo1/listados/viajes_proximos.html",{'lista':lista_viajes_proximos, 'valor': True if len(lista_viajes_proximos)!=0 else False,"mensaje":mensaje})

def pasajeros_de_viajes_proximos(request, pk):
    lista= Pasaje.objects.filter(activo=True,estado="PENDIENTE", viaje_id=pk)
    return render(request, "demo1/listados/pasajeros_viajes_proximos.html",{'lista':lista, 'valor': True if len(lista)!=0 else False})

def obtener_viaje_en_curso(chofer):
    viajes=Viaje.objects.filter(activo=True).filter(estado='ENCURSO')
    if viajes.exists():
        for viaje in viajes:
            if viaje.ruta.combi.chofer.id ==chofer.id:
                return viaje.id
    return -1

def vender_pasaje_en_curso(request):
    pass


