import json
from django.db.models.fields import BLANK_CHOICE_DASH
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import FormLugar,FormPasajeroModi, FormPasajeroModi2,FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormTarjeta, FormoBusquedaViaje ,FormComentario, FormChoferModi
from datetime import date, datetime
from django.core.paginator import Paginator
from .models import Chofer, Pasaje, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona,Comentario
from django.contrib.auth.hashers import make_password

dicPasajeros1 = {0:0}
dicPasajeros2 = {0:0}


def verificarLetra(string):
	for l in string:
		sigue=False
		c=65
		for i in range(25):
			if ord(l.upper())==c:
				sigue=True
			c+=1
		if not sigue:
			return False
	return True
	
def verificarNumero(num):
	try: 
		n=int(num)
		return True
	except:
		return False
		
def verificarPatente(patente):
	if len(patente)==6:
		if verificarLetra(patente[0:3]) and verificarNumero(patente[3:6]):
			return True
		else:
			return False
	elif len(patente)==7:
		if verificarLetra(patente[0:2]) and verificarNumero(patente[2:5]) and verificarLetra(patente[5:7]):
			return True
		else:
			return False
	else:
		return False

def principal(request):
    administrador = User.objects.filter(is_superuser=True)   
    return render(request, 'demo1/principal.html', {'administrador': administrador})

def detalle_usuario(request, pk):
    usuario = User.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_usuario.html', {'usuario': usuario})

def no_se_encuentra_en_combi(pk):
    queryset = Combi.objects.filter(activo=True).values_list('chofer_id',flat=True)
    if pk in queryset:
        return False
    else:
        return True

def obtenerChoferes():
    choferes= Chofer.objects.filter(activo=True).values()
    lista=[]
    for i in choferes:
        user=User.objects.get(id=i['usuario_id'])
        d=no_se_encuentra_en_combi(i['id'])
        dic={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email, 'pk':i['id'],"puede":d}
        lista.append(dic)
    return lista

def listadoDePaginacion(lista, request):
    paginator= Paginator(lista, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    return (paginator.get_page(page_number), cantidad)

def listado_chofer(request):
    choferes= obtenerChoferes() 
    page_obj,cantidad = listadoDePaginacion(choferes, request)
    return render(request, 'demo1/listados/listado_chofer.html', {'page_obj':page_obj, 'cantidad':cantidad})

def verificarSiCombiValido(id):
    viajes=Viaje.objects.filter(activo=True).values()
    for i in viajes:
        ruta=Ruta.objects.filter(id=i['ruta_id']).values()
        if ruta[0]['combi_id']==id:
            return False
    return True

def filaDeCombi():
    combis=Combi.objects.filter(activo=True).values()
    lista=[]
    for c in combis:
        chofer=Chofer.objects.filter(id=c['chofer_id']).values()
        n=verificarSiCombiValido(c['chofer_id'])
        d=User.objects.filter(id=chofer[0]['usuario_id']).values()
        dic={'modelo': c['modelo'], 'patente':c['patente'], 'chofer': d[0]['first_name']+' '+d[0]['last_name'], 'pk':c['id'], 'sePuede':n}
        lista.append(dic)
    return lista

def listado_combi(request):
    combis=filaDeCombi()
    page_obj,cantidad = listadoDePaginacion(combis, request)
    return render(request, 'demo1/listados/listado_combi.html', {'page_obj':page_obj, 'cantidad':cantidad, 'noSePuede':False})

def lisatdo_pasajero(request):
    pasajeros=Pasajero.objects.all()
    return render(request, 'demo1/listados/listado_pasajero.html', {'pasajeros':pasajeros})

def obtenerValorUnLugar(id):
    rutas=Ruta.objects.filter(activo=True).values()
    for i in rutas:
        if i['origen_id']==id or i['destino_id']==id:
            return False
    return True

def obtenerListaDeLugares():
    lugares=Lugar.objects.filter(activo=True).values()
    lista=[]
    for l in lugares:
        d=obtenerValorUnLugar(l['id'])
        dic={'nombre_de_lugar':l['nombre_de_lugar'], 'provincia':l['provincia'], 'valor':d, 'pk':l['id']}
        lista.append(dic)
    return lista

def listado_lugar(request):
    lugares=obtenerListaDeLugares()
    page_obj,cantidad = listadoDePaginacion(lugares, request)
    return render(request, 'demo1/listados/listado_lugar.html', {'page_obj':page_obj, 'cantidad':cantidad})

def verificarInsumoEnViaje(pk):
    """
    hoy= date.today()
    pasajes=Pasaje.objects.filter(activo=True)
    for i in pasajes:
        if i.viaje.fecha >= hoy and i.cantInsumos.count()!=0:
            for j in i.cantInsumos:
                if j.insumo.pk==pk:
                    return False
    """
    return True

def listado_insumo(request):
    insumos=Insumo.objects.filter(activo=True)
    page_obj,cantidad = listadoDePaginacion(insumos, request)
    return render(request, 'demo1/listados/listado_insumo.html',{'page_obj':page_obj, 'cantidad':cantidad, 'noSeElimina':False, 'noModificado':False})

def verficarRuta2(pk):
        viajes=Viaje.objects.filter(activo=True)
        ruta = Ruta.objects.get(pk=pk)
        for v in viajes:
            if ruta.id==v.ruta.id and v.fecha>=date.today():
                return False
        return True

def obtenerOrigenesDestino():
    rutas=Ruta.objects.filter(activo=True)
    lista=[]
    for r in rutas:
        o=Lugar.objects.get(id=r.origen.id)
        d=Lugar.objects.get(id=r.destino.id)
        dic={'origen': o.nombre_de_lugar+', '+o.provincia, 'destino': d.nombre_de_lugar+', '+d.provincia, 'hora':r.hora, 'pk':r.id }
        lista.append(dic)
    return lista

def listado_ruta(request):
    rutas=obtenerOrigenesDestino()
    page_obj,cantidad = listadoDePaginacion(rutas, request)
    return render(request, 'demo1/listados/listado_ruta.html',{'page_obj':page_obj, 'cantidad':cantidad})

def armarFilaViaje():
    lista=[]
    viajes=Viaje.objects.filter(activo=True).values()
    for v in viajes:
        r=Ruta.objects.filter(id=v['ruta_id']).values()
        combi=Combi.objects.filter(id=r[0]['combi_id']).values()
        o=Lugar.objects.filter(id=r[0]['origen_id']).values()
        d=Lugar.objects.filter(id=r[0]['destino_id']).values()
        dic={'patente':combi[0]['patente'], 'origen':o[0]['nombre_de_lugar'], 'destino':d[0]['nombre_de_lugar'],
            'hora': r[0]['hora'], 'distancia':r[0]['distancia'], 'cant': v['asientos'], 'fecha':v['fecha'], 'precio':v['precio'], 'pk':v['id']}
        lista.append(dic)
    return lista

def listado_viaje(request):
    viajes=armarFilaViaje()
    page_obj,cantidad = listadoDePaginacion(viajes, request)
    return render(request, 'demo1/listados/listado_viaje.html', {'page_obj':page_obj, 'cantidad':cantidad})

def compararLugar(d):
    lugares= Lugar.objects.filter(activo=True).values()
    for l in lugares:
        if l['nombre_de_lugar'].upper()==d['nombre'].upper() and l['provincia'].upper()==d['provincia'].upper():
            return False
    return True

def compararLugarModificado(d,pk):
    lugares= Lugar.objects.filter(activo=True).exclude(pk=pk).values()
    for l in lugares:
        if l['nombre_de_lugar'].upper()==d['nombre'].upper() and l['provincia'].upper()==d['provincia'].upper():
            return False
    return True

def lugar_new(request):
    exitoso=False
    fallido=False
    if request.method == "POST":
        form = FormLugar(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            if compararLugar(datos):
                lugar = Lugar.objects.create()
                lugar.nombreYprovincia(datos['nombre'],datos['provincia'])
                lugar.save()
                exitoso=True
            else:
                fallido=True
    else:
        form = FormLugar()
    return render(request, 'demo1/form/formulario_lugar.html', {'form': form, 'exitoso':exitoso, 'fallido':fallido})

def fecha_vencimiento_es_valida(fecha_de_vencimiento):
    hoy=date.today()
    return fecha_de_vencimiento > hoy

def tarjeta_new(request,pk):
    exitoso=False
    fecha_vencimiento_no_es_valida=False
    if request.method=="POST":
        form=FormTarjeta(request.POST)
        if form.is_valid():
            p=dicPasajeros1[pk]
            t=form.cleaned_data
            if fecha_vencimiento_es_valida(t["fecha_de_vencimiento"]):
                usuario=User.objects.create(is_superuser=False,password=p["password"],email=p["email"],first_name=p["first_name"],last_name=p["last_name"])
                usuario.username=usuario.id
                usuario.password=make_password(p["password"])
                usuario.save()
                pasajero=Pasajero.objects.create(usuario=usuario,dni=int(p["dni"]),telefono=int(p["telefono"]),tipo=p["tipo"],fecha_de_nacimiento=p["fecha_de_nacimiento"])
                pasajero.save()
                tarjeta=Tarjeta.objects.create(pasajero=Pasajero.objects.last(),numero=t["numero"],fecha_de_vencimiento=t["fecha_de_vencimiento"],codigo=t["codigo"],activo=True)
                tarjeta.save()
                exitoso=True
                #del dicPasajeros1[pk]
            else:
                fecha_vencimiento_no_es_valida=True
    else:
        form=FormTarjeta()
    return render(request,'demo1/form/formulario_tarjeta.html',{"form":form,"exitoso":exitoso,"fv":fecha_vencimiento_no_es_valida}) 

def tarjeta_new_modificado(request,pk):
    exitoso=False
    fecha_vencimiento_no_es_valida=False
    tarjetaRep=False
    p=dicPasajeros2[pk]
    pasajero= buscar_pasajero_dni(p["dni"])
    login(request, pasajero.usuario)
    tiene= tiene_tarjeta(pasajero.pk)
    if request.method=="POST":
        form=FormTarjeta(request.POST)
        if form.is_valid():
            t=form.cleaned_data
            if tiene:
                tarj= obtener_tarjeta(pasajero.pk)
            if fecha_vencimiento_es_valida(t["fecha_de_vencimiento"]):
                if tiene:
                    tarjeta=tarj
                    tarjeta.numero=t['numero']
                    tarjeta.fecha_de_vencimiento= t["fecha_de_vencimiento"]
                    tarjeta.codigo=t['codigo']
                else:
                    tarjeta=Tarjeta.objects.create(pasajero=pasajero,numero=t["numero"],fecha_de_vencimiento=t["fecha_de_vencimiento"],codigo=t["codigo"],activo=True)
                pasajero.tipo=p["tipo"]
                pasajero.save()
                tarjeta.save()
                exitoso=True
                    
            else:
                fecha_vencimiento_no_es_valida=True
    else:
        form=FormTarjeta()
    return render(request,'demo1/form/formulario_tarjeta_modificado.html',{"form":form,"exitoso":exitoso,"fv":fecha_vencimiento_no_es_valida,'tarjetaRep':tarjetaRep,'user':pasajero.usuario})

def calcular_edad(p):
    hoy=date.today()
    edad=hoy.year - p["fecha_de_nacimiento"].year
    edad-=((hoy.month,hoy.day)<(p["fecha_de_nacimiento"].month,p["fecha_de_nacimiento"].day))
    return edad

def calcular_edad2(fechaNac):
    hoy=date.today()
    edad=hoy.year - fechaNac.year
    edad-=((hoy.month,hoy.day)<(fechaNac.month,fechaNac.day))
    return edad

def pasajero_new(request):
    dicPasajeros1[0] += 1
    exitoso=False
    fallido=False
    tipo=False
    edad=0
    dniUnico=True
    mailUnico=True
    if request.method=="POST":
        form=FormPasajero(request.POST)
        if form.is_valid():
            p=form.cleaned_data
            edad=calcular_edad(p)
            dniUnico= not Persona.objects.filter(dni=(p["dni"])).exists()
            mailUnico= not User.objects.filter(email=(p["email"])).exists()
            if (edad>=18 and dniUnico and mailUnico):
                if p["tipo"]=="BASICO":
                    usuario=User.objects.create(is_superuser=False,password=p["password"],email=p["email"],first_name=p["first_name"],last_name=p["last_name"])
                    usuario.username=usuario.id
                    usuario.password=make_password(p["password"])
                    usuario.save()
                    pasajero=Pasajero.objects.create(usuario=usuario,dni=int(p["dni"]),telefono=int(p["telefono"]),tipo=p["tipo"],fecha_de_nacimiento=p["fecha_de_nacimiento"])
                    pasajero.save()
                    tipo=True
                    exitoso=True
                else:
                    dicPasajeros1[dicPasajeros1[0]]=p
                    return redirect('registrar_tarjeta',dicPasajeros1[0])
            else:
                fallido=True
    else:
        form=FormPasajero()
    return render(request,'demo1/form/formulario_usuario.html',{"form":form,"edad":edad,"exitoso":exitoso,"tipo":tipo,"dniUnico":dniUnico,"mailUnico":mailUnico,"fallido":fallido,'pk':dicPasajeros1[0]}) 

def buscar_pasajero(pk):
    queryset=Pasajero.objects.filter(activo=True)
    for pasajero in queryset:
        if pasajero.usuario.id == pk:
            return pasajero

def buscar_pasajero_dni(dni):
    queryset=Pasajero.objects.filter(activo=True)
    for pasajero in queryset:
        if pasajero.dni == int(dni):
            return pasajero

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
    

def modificar_pasajero(request,pk):
    dicPasajeros2[0] += 1
    pasajero= buscar_pasajero(pk)
    exitoso=False
    tipo=False
    pasajeropk=pasajero.pk
    edad=calcular_edad2(pasajero.fecha_de_nacimiento)
    dniUnico=True
    mailUnico=True
    if pasajero.tipo=="BASICO":
        if request.method=="GET":
            data= {'username':pasajero.usuario.username,'email':pasajero.usuario.email,'first_name':pasajero.usuario.first_name,'last_name':pasajero.usuario.last_name,'dni':pasajero.dni,'telefono':pasajero.telefono,'tipo':pasajero.tipo,'fecha_de_nacimiento':pasajero.fecha_de_nacimiento}
            form=FormPasajeroModi2(data)
        else:
            form=FormPasajeroModi2(request.POST)
            if form.is_valid():
                p=form.cleaned_data
                edad=calcular_edad(p)
                dniUnico= not Persona.objects.exclude(pk=pasajeropk).filter(dni=(p["dni"])).exists()
                mailUnico= not User.objects.exclude(pk=pk).filter(email=(p["email"])).exists()
                if (edad>=18 and dniUnico and mailUnico):
                    pasajero.usuario.email=p["email"]
                    pasajero.usuario.first_name=p["first_name"]
                    pasajero.usuario.last_name=p["last_name"]
                    pasajero.usuario.username=pasajero.usuario.id
                    pasajero.usuario.save()
                    pasajero.dni=int(p["dni"])
                    pasajero.telefono=int(p["telefono"])
                    pasajero.fecha_de_nacimiento=p["fecha_de_nacimiento"]
                    pasajero.save()
                    tipo=True
                    exitoso=True
                    if p["tipo"]=="GOLD":
                        dicPasajeros2[dicPasajeros2[0]]=p
                        return redirect('registrar_tarjeta_modificado',dicPasajeros2[0])
            
        return render(request,'demo1/modificar/formulario_modificar_pasajero.html',{"form":form,'pk':dicPasajeros2[0],"edad":edad,"exitoso":exitoso,"dniUnico":dniUnico,"mailUnico":mailUnico})
    else:
        
        tarjetaRep=False
        vencNoValida=False
        tarjeta= obtener_tarjeta(pasajeropk)
        data= {'username':pasajero.usuario.username,'email':pasajero.usuario.email,'first_name':pasajero.usuario.first_name,'last_name':pasajero.usuario.last_name,'dni':pasajero.dni,'telefono':pasajero.telefono,'tipo':pasajero.tipo,'fecha_de_nacimiento':pasajero.fecha_de_nacimiento,'numero':tarjeta.numero,'fecha_de_vencimiento':tarjeta.fecha_de_vencimiento,'codigo':tarjeta.codigo}
        if request.method=="GET":
            form=FormPasajeroModi(data)
        else:
            form=FormPasajeroModi(request.POST)
            if form.is_valid():
                p=form.cleaned_data
                edad=calcular_edad(p)
                dniUnico= not Persona.objects.exclude(pk=pasajeropk).filter(dni=(p["dni"])).exists()
                mailUnico= not User.objects.exclude(pk=pk).filter(email=(p["email"])).exists()
                if (edad>=18 and dniUnico and mailUnico):
                    if fecha_vencimiento_es_valida(p["fecha_de_vencimiento"]):
                        pasajero.usuario.email=p["email"]
                        pasajero.usuario.first_name=p["first_name"]
                        pasajero.usuario.last_name=p["last_name"]
                        pasajero.usuario.username=pasajero.usuario.id
                        pasajero.usuario.save()
                        pasajero.dni=int(p["dni"])
                        pasajero.telefono=int(p["telefono"])
                        pasajero.tipo=p["tipo"]
                        pasajero.fecha_de_nacimiento=p["fecha_de_nacimiento"]
                        pasajero.save()
                        exitoso=True
                        tarjeta.numero = p["numero"]
                        tarjeta.codigo = p["codigo"]
                        tarjeta.fecha_de_vencimiento = p["fecha_de_vencimiento"]
                        tarjeta.save()
                        if p["tipo"]=="BASICO":
                            return redirect('modificar_pasajero',pk)
                        else:
                            vencNoValida=True
        return render(request,'demo1/modificar/formulario_modificar_pasajero.html',{"form":form,'pk':pk,"tarjetaRep":tarjetaRep,"vencNoValida":vencNoValida,"edad":edad,"exitoso":exitoso,"dniUnico":dniUnico,"mailUnico":mailUnico}) 


def tarjetaRepetidaModificado(pk,numero):
    return Tarjeta.objects.exclude(pk=pk).filter(activo=True).filter(numero=numero).exists()

def tarjetaRepetida(numero):
    return Tarjeta.objects.filter(activo=True).filter(numero=numero).exists()


def es_fallo_usuario(email):
    try:
        User.objects.get(email=email)
        return False
    except:
        return True

def buscar_id_con_email(email):
    try:
        usuario=User.objects.get(email=email)
        return usuario.id
    except:
        return -1

def es_pasajero(user):
    persona=Persona.objects.get(usuario_id=user.id)
    try:
        Pasajero.objects.get(persona_ptr_id=persona.id)
        return True
    except:
        return False

def es_admin(user):
    return user.is_superuser or user.is_staff

def viajesEnCurso(chofer):
    viajes=Viaje.objects.filter(activo=True).filter(estado='ENCURSO')
    if viajes.exists():
        for viaje in viajes:
            if viaje.ruta.combi.chofer.id ==chofer.id:
                return True
    return False

def buscar_chofer(pk):
    queryset=Chofer.objects.filter(activo=True)
    for chofer in queryset:
        if chofer.usuario.id == pk:
            return chofer

def login_usuario(request):
    fallo_usuario=False
    fallo_password=False
    if request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            id=buscar_id_con_email(email)
            user = authenticate(username=id,password=password)
            if user is not None:
                login(request, user)
                if es_admin(user):
                    return redirect("http://127.0.0.1:8000/")
                elif es_pasajero(user):
                    return redirect("http://127.0.0.1:8000/home_usuario/")
                else:
                    return redirect("http://127.0.0.1:8000/home_usuario_chofer/")            
            elif es_fallo_usuario(email):
                fallo_usuario=True
            else:
                fallo_password=True
    else:
        form = FormLogin()
    return render(request, "demo1/login.html", {"form":form,"falloU":fallo_usuario,"falloP":fallo_password})

def retornar_usuario(id_pasajero):
    persona=Persona.objects.get(id=id_pasajero)
    usuario=User.objects.get(id=persona.usuario_id)
    return usuario

def obtenerComentarios(user):
    comentarios= Comentario.objects.filter(activo=True).values()
    lista=[]
    for i in comentarios:
        usuario=retornar_usuario(i["pasajero_id"])
        valor=True if usuario.pk==user.pk else False
        dic={'texto':i["texto"], 'fecha':i["fecha"], 'hora':i["hora"], 'id':i["id"],'first_name':usuario.first_name, 'last_name':usuario.last_name, 'valor':valor}
        lista.append(dic)
    return lista

def home_usuario(request, pk=None):
    if pk!=None:
        comentar=Comentario.objects.get(id=pk)
        comentar.activo=False
        comentar.save()
    comentarios=obtenerComentarios(request.user)
    comentarios=sorted(comentarios,key=lambda item: (item["fecha"],item["hora"]),reverse=True )
    page_obj,cantidad = listadoDePaginacion(comentarios, request)
    return render(request,"demo1/home_usuario.html",{'page_obj':page_obj, 'cantidad':cantidad})

def home_usuario_chofer(request):
    enCurso=False
    if viajesEnCurso(buscar_chofer(request.user.pk)):
        enCurso=True
    return render(request,"demo1/home_usuario_chofer.html", {"enCurso":enCurso})

def logout_usuario(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/login/")

def chofer_new(request):
    exitoso=False
    dniUnico=True
    mailUnico=True
    if request.method=="POST":
        form=FormChofer(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            dniUnico= not Persona.objects.filter(dni=(d["dni"])).exists()
            mailUnico= not User.objects.filter(email=(d["email"])).exists()
            if dniUnico and mailUnico:
                user= User.objects.create(email=d['email'], password=d['password'], first_name=d['first_name'], last_name=d['last_name'], is_staff=False)
                user.password=make_password(d["password"])
                user.username=user.id
                user.save()
                chofer= Chofer.objects.create(dni=int(d['dni']), telefono=d['telefono'], usuario=user)
                chofer.save()
                exitoso=True
            else: 
                p=Persona.objects.filter(dni=(d["dni"]), activo=False)
                u=User.objects.filter(email=(d["email"]))
                fercho=None
                if p.count()!=0:
                    fercho=Chofer.objects.get(persona_ptr_id=p[0].pk)
                else:
                    fercho=Chofer.objects.get(usuario_id=u[0].pk)
                if not fercho.activo:
                    fercho.usuario.email= d['email']
                    fercho.usuario.password=make_password(d["password"])
                    fercho.usuario.first_name=d['first_name']
                    fercho.usuario.last_name= d['last_name']
                    fercho.usuario.is_staff=False
                    fercho.usuario.username=fercho.usuario.id
                    fercho.usuario.save()
                    fercho.dni=d['dni']
                    fercho.telefono=d['telefono']
                    fercho.activo=True
                    fercho.save()
                    dniUnico=True
                    mailUnico=True
                    exitoso=True
    else:
        form=FormChofer()
    return render(request,'demo1/form/formulario_chofer.html',{"form":form,"exitoso": exitoso,'dniUnico':dniUnico,'mailUnico':mailUnico})

def verficarChofer(idChofer):
    dato=Combi.objects.filter(chofer=idChofer.pk, activo=True)
    if dato.count()!= 0:
        return False
    return True

def verificarPatenteEnCombis(unaPatente):
    combi=Combi.objects.filter(patente=unaPatente, activo=True)
    if combi.count()==0:
        return True
    return False

def combi_new(request):
    valor=False
    exitoso=False
    patenteInvalido=False
    if request.method=='POST':
        form=FormCombi(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            c=verficarChofer(d['chofer'])
            p=verificarPatente(d['patente'])
            patente=verificarPatenteEnCombis(d['patente'])
            if c and p and patente:
                combi=Combi.objects.create(chofer=d['chofer'], modelo=d['modelo'], asientos=d['cantAsientos'], patente=d['patente'], tipo=d['tipo'],activo=True)
                combi.save()
                exitoso=True
            if not c:
                valor=True
            if not p or not patente:
                patenteInvalido=True
    else:
        form=FormCombi()
    return render(request, 'demo1/form/formulario_combi.html', {'form': form, 'valor': valor, 'exitoso':exitoso, 'patenteInvalido':patenteInvalido})

def verificarFechaYRuta(unaFecha, ruta,pk=None):
    if pk != None:
        return not Viaje.objects.exclude(pk=pk).filter(activo=True).filter(fecha=unaFecha).filter(ruta=ruta.pk).exists()
    return not Viaje.objects.filter(activo=True).filter(fecha=unaFecha).filter(ruta=ruta.pk).exists()

def verifivarAsientos(d):
    ruta2=Ruta.objects.get(id=d['ruta'].pk)
    unaCombi=Combi.objects.get(id=ruta2.combi.pk)
    dato= True if d['asientos'] <=unaCombi.asientos else False
    return dato

def es_fecha_valida(fecha):
    return fecha > date.today()

def viaje_new(request):
    valor=False
    exitoso=False
    pasado=False
    asientosValidos=False
    if request.method=='POST':
        form=FormViaje(request.POST)
        if form.is_valid():
            d=form.cleaned_data  
            a=verificarFechaYRuta(d['fecha'], d['ruta'])
            v=verifivarAsientos(d)
            p=es_fecha_valida(d["fecha"])
            if a and v and p:
                unaRuta=Ruta.objects.get(id=d['ruta'].pk)  
                viaje=Viaje.objects.create(ruta=unaRuta, fecha=d['fecha'], precio=d['precio'], asientos= d['asientos'],activo=True)
                viaje.save()
                exitoso=True
            if not a:
                valor=True 
            if not v:
                asientosValidos=True
            if not p:
                pasado=True
    else:
        form=FormViaje()
    return render(request, 'demo1/form/formulario_viaje.html', {'form': form, 'valor':valor, 'exitoso':exitoso, 'asientosValidos':asientosValidos,"pasado":pasado})

def verificarInsumo(datos):
    insumos=Insumo.objects.filter(activo=True)
    for i in insumos:
        if i.nombre.upper()==datos['nombre'].upper():
            return False
    return True

def verificarInsumoModificado(datos,pk):
    insumos=Insumo.objects.filter(activo=True).exclude(pk=pk)
    for i in insumos:
        if i.nombre.upper()==datos['nombre'].upper():
            return False
    return True

def insumo_new(request):
    valor=False
    exitoso=False
    if request.method=='POST':
        form=FormInsumo(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            if verificarInsumo(d):   
                insumo=Insumo.objects.create(tipo=d['tipo'], nombre=d['nombre'],precio=d['precio'])
                insumo.save()
                exitoso=True
            else: 
                valor=True
    else:
        form=FormInsumo()
    return render(request, 'demo1/form/formulario_insumo.html', {'form': form, 'valor':valor, 'exitoso':exitoso})

def verificarHoraYRuta(d):
    dato=Ruta.objects.filter(origen = d['origen'].pk, destino= d['destino'].pk,activo=True)
    if dato.count() !=0:
        if dato[0].hora.hour==d['hora'].hour:
            return True
    return False

def ruta_new(request):
    exitoso=False
    desOriEquls=False
    rutaRep = False
    if request.method=='POST':
        form=FormRuta(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            desOriEquls= d['origen'].pk == d['destino'].pk
            rutaRep = verificarHoraYRuta(d)
            if not desOriEquls and not rutaRep:
                ruta=Ruta.objects.create(combi=d['combi'], origen=d['origen'], destino=d['destino'], distancia=d['distancia'], hora=d['hora'],activo=True)
                ruta.save()
                exitoso=True
            return render(request, 'demo1/form/formulario_ruta.html', {'form': form, 'desOriEquls':desOriEquls, 'rutaRep':rutaRep,'exitoso':exitoso})
    else:
        form=FormRuta()
    return render(request, 'demo1/form/formulario_ruta.html', {'form': form, 'desOriEquls':desOriEquls, 'rutaRep':rutaRep,'exitoso':exitoso})

def buscar_pasajero(id_u):
    persona=Persona.objects.get(usuario_id=id_u)
    try:
        pasajero=Pasajero.objects.get(persona_ptr_id=persona.id)
        return pasajero
    except:
        return None

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

def tiene_viajes(pasajero):
    viajes=Viaje.objects.filter(pk__in=(list(set(Pasaje.objects.filter(estado="PASADO",pasajero_id=pasajero.id).values_list('viaje', flat=True)))))
    if len(viajes)>0:
        return True
    else:
        return False
    

def comentario_new(request):
    exitoso=False
    fallido=False
    if request.method=="POST":
        form=FormComentario(request.POST)
        if form.is_valid():
            c=form.cleaned_data
            pasajero=buscar_pasajero(request.user.id)
            if tiene_viajes(pasajero):
                if len (c["texto"])>115:
                    texto=armar_texto(c["texto"])
                else:
                    texto=c["texto"]
                comentario=Comentario.objects.create(texto=texto,pasajero=pasajero,fecha=date.today(),hora=datetime.now().time())
                comentario.save()
                exitoso=True
            else:
                fallido=True
    else:        
        form=FormComentario()
    return render(request,'demo1/form/formulario_comentario.html',{'form':form,'exitoso':exitoso,"fallido":fallido})

def es_pendiente(viaje,id_pasajero):
    try:
        Pasaje.objects.get(viaje_id=viaje.id,estado="PENDIENTE",pasajero_id=id_pasajero)
        return True
    except:
        return False

def detalle_chofer(request, pk):
    print('detalle ',pk)
    chofer = Chofer.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_chofer.html', {'chofer': chofer})

def detalle_combi(request, pk):
    combi = Combi.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_combi.html', {'combi': combi})

def modificar_ruta(request,pk):
    noModificado=False
    if verficarRuta2(pk):
        ruta = Ruta.objects.get(pk=pk)
        data = {'combi': ruta.combi,'origen': ruta.origen,'destino': ruta.destino,'hora': ruta.hora,'distancia': ruta.distancia}
        desOriEquls=False
        rutaRep=False
        if request.method=='GET':
            form=FormRuta(data)
        else:
            form=FormRuta(request.POST)
            if form.is_valid():
                d=form.cleaned_data 
                unOrigen=d['origen']
                unDestino=d['destino']
                unaCombi= d['combi']
                desOriEquls= unOrigen.id == unDestino.id
                rutaRep = verificarHoraYRuta(d)
                if not desOriEquls and not rutaRep:
                    ruta.origen=unOrigen
                    ruta.destino=unDestino
                    ruta.combi=unaCombi
                    ruta.hora= d['hora']
                    ruta.distancia= d['distancia']
                    ruta.save()
                    return redirect('listado_ruta')   
        return render(request, 'demo1/modificar/formulario_modificar_ruta.html', {'form': form,'desOriEquls':desOriEquls,'rutaRep':rutaRep})
    else:
        noModificado=True
        rutas=obtenerOrigenesDestino()
        page_obj,cantidad = listadoDePaginacion(rutas, request)
        return render(request, 'demo1/listados/listado_ruta.html',{'page_obj':page_obj, 'cantidad':cantidad, 'noModificado':noModificado})

def modificar_insumo(request,pk):
    noModificado=False
    if verificarInsumoEnViaje(pk):
        insumo = Insumo.objects.get(pk=pk)
        if request.method=='POST':
            form=FormInsumo(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                if verificarInsumoModificado(d,pk):
                    insumo.tipo = d['tipo']
                    insumo.nombre = d['nombre']
                    insumo.precio = d['precio']
                    insumo.save()
                    return redirect('listado_insumo') 
                else:
                    noModificado=True
                    return render(request, 'demo1/modificar/formulario_modificar_insumo.html', {'form': form,'noModificado':noModificado})
        else:
            data = {'tipo': insumo.tipo,'nombre': insumo.nombre,'precio': insumo.precio}
            form=FormInsumo(data)
        return render(request, 'demo1/modificar/formulario_modificar_insumo.html', {'form': form})
    else:
        noModificado=True
        insumos=Insumo.objects.filter(activo=True)
        page_obj,cantidad = listadoDePaginacion(insumos, request)
        return render(request, 'demo1/listados/listado_insumo.html',{'page_obj':page_obj, 'cantidad':cantidad, 'noModificado':noModificado})


def detalle_lugar(request, pk):
    lugar = Lugar.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_lugar.html', {'lugar': lugar})

def modificar_lugar(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    noModificado=False
    if obtenerValorUnLugar(lugar.id):
        if request.method == "POST":
            form = FormLugar(request.POST)
            if form.is_valid():
                datos = form.cleaned_data
                if compararLugarModificado(datos,pk):
                    if datos['nombre']!='' and datos['provincia']!='':
                        lugar.nombreYprovincia(datos['nombre'],datos['provincia'])
                        lugar.save()
                        return redirect('listado_lugar')
                else:
                    noModificado=True
                    
        else:
            data = {'nombre': lugar.nombre_de_lugar,'provincia': lugar.provincia}
            form = FormLugar(data)
        return render(request, 'demo1/modificar/formulario_modificar_lugar.html', {'form': form,'noModificado':noModificado})
    else:
        noModificado=True
        lugares=obtenerListaDeLugares()
        page_obj,cantidad = listadoDePaginacion(lugares, request)
        return render(request, 'demo1/listados/listado_lugar.html', {'page_obj':page_obj, 'cantidad':cantidad,'noModificado':noModificado})

def eliminar_chofer(request, pk):
    chofer = Chofer.objects.filter(pk=pk)
    noEliminado=False
    if(no_se_encuentra_en_combi(pk)):
        for object in chofer:
            object.activo = False
            object.save()
    else:
        noEliminado=True
    dato=json.dumps([{"seElimino":noEliminado,
                        "mensaje":"No fue posible borrar al chofer ya que se encuentra asignado a una combi"}])
    return HttpResponse(dato, 'application/json')
    
def eliminar_combi(request, pk):
    noEliminado=True
    if no_se_encuentra_en_ruta(pk):
        combi = Combi.objects.get(pk=pk)
        combi.activo = False
        combi.save()
        noEliminado=False
    dato=json.dumps([{"seElimino":noEliminado,
                        "mensaje":"No es posible borrar la combi ya que se encuentra asignado a una ruta"}])
    return HttpResponse(dato, 'application/json')

def no_tieneViajesVendidos(pk):
    elviaje=Viaje.objects.get(pk=pk)
    if elviaje.fecha < date.today():
        return True
    else:
        return Viaje.objects.get(pk=pk).vendidos == 0 

def eliminar_viaje(request, pk):
    viaje = Viaje.objects.get(pk=pk)
    exitoso=True
    if no_tieneViajesVendidos(pk):
        viaje.activo = False
        viaje.save()
        exitoso=False
    dato=json.dumps([{"seElimino":exitoso,
                        "mensaje":"No se realizo la eliminacion porque hay al menos un pasaje vendido"}])
    return HttpResponse(dato, 'application/json')

def eliminar_ruta(request, pk):
    exitosoE=True
    if verficarRuta2(pk):
        ruta = Ruta.objects.get(pk=pk)
        ruta.activo = False
        ruta.save()
        exitosoE=False
    dato=json.dumps([{"seElimino":exitosoE,
                "mensaje":"La ruta que desea eliminar esta en un viaje presente o futuro, no se realizo la eliminación"}])
    return HttpResponse(dato, "application/json")

def eliminar_insumo(request, pk):
    if verificarInsumoEnViaje(pk):
        insumo = Insumo.objects.get(pk=pk)
        insumo.activo = False
        insumo.save()
    dato=json.dumps([{"seElimino":False,
                        "mensaje":""}])
    return HttpResponse(dato, 'application/json')

def eliminar_lugar(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    fallido=True
    if obtenerValorUnLugar(lugar.id):
        lugar.activo = False
        lugar.save()
        fallido=False
    dato=json.dumps([{"seElimino":fallido,
                        "mensaje":"No fue posible borrar el lugar ya que se encuentra en una ruta"}])
    return HttpResponse(dato, 'application/json')
  
def detalle_tarjeta(request, pk):
    tarjeta = Tarjeta.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_tarjeta.html', {'tarjeta': tarjeta})

def modificar_chofer(request,pk):
    noModificado=False
    if(no_se_encuentra_en_combi(pk)):
        dniUnico=True
        mailUnico=True
        fercho = Chofer.objects.get(pk=pk)
        data = {'email':fercho.usuario.email,'password':'','first_name':fercho.usuario.first_name,'last_name':fercho.usuario.last_name,'username':fercho.usuario.username,'dni':fercho.dni,'telefono':fercho.telefono}
        if request.method=="GET":
            form=FormChoferModi(data)
        else:
            form=FormChoferModi(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                userpk=fercho.usuario.pk
                dniUnico= not Persona.objects.exclude(pk=pk).filter(dni=(d["dni"])).exists()
                mailUnico= not User.objects.exclude(pk=userpk).filter(email=(d["email"])).exists()
                if dniUnico and mailUnico:
                    fercho.usuario.email= d['email']
                    fercho.usuario.password=make_password(d["password"])
                    fercho.usuario.first_name=d['first_name']
                    fercho.usuario.last_name= d['last_name']
                    fercho.usuario.is_staff=False
                    fercho.usuario.username=fercho.usuario.id
                    fercho.usuario.save()
                    fercho.dni=d['dni']
                    fercho.telefono=d['telefono']
                    fercho.save()
                    return redirect('listado_chofer')
        return render(request,'demo1/modificar/formulario_modificar_chofer.html',{"form":form,'dniUnico':dniUnico,'mailUnico':mailUnico})
    else:
        noModificado = True
        user= obtenerChoferes() 
        page_obj,cantidad = listadoDePaginacion(user, request)
        return render(request, 'demo1/listados/listado_chofer.html', {'page_obj':page_obj, 'cantidad':cantidad,"noModificado":noModificado})


def modificar_viaje(request,pk):
    viaje= Viaje.objects.get(pk=pk)
    asientosValidos=True
    viajeValido=True
    noModificado=False
    pasado=False
    exitoso=True
    if no_tieneViajesVendidos(pk):
        data= {'ruta':viaje.ruta,'fecha':viaje.fecha,'precio':viaje.precio,'asientos':viaje.asientos}
        if request.method=='GET':
            form=FormViaje(data)
        else:
            form=FormViaje(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                viajeValido=verificarFechaYRuta(d['fecha'], d['ruta'],pk)
                asientosValidos= viaje.ruta.combi.asientos >= d['asientos']
                p=es_fecha_valida(d["fecha"])
                if viajeValido and asientosValidos and p:
                    viaje.ruta=d['ruta']
                    viaje.fecha=d['fecha']
                    viaje.precio= d['precio']
                    viaje.asientos=d['asientos']
                    viaje.save()
                    return redirect('listado_viaje')
                elif not p:
                    pasado=True
        return render(request, 'demo1/modificar/formulario_modificar_viaje.html', {'form': form, 'asientosValidos':asientosValidos,'viajeValido':viajeValido,'capacidad':str(viaje.ruta.combi.asientos),"pasado":pasado}) 
    else:
        noModificado=True
        viajes=armarFilaViaje()
        page_obj,cantidad = listadoDePaginacion(viajes, request)
        return render(request, 'demo1/listados/listado_viaje.html', {'page_obj':page_obj, 'cantidad':cantidad,'noModificado':noModificado})

def no_se_encuentra_en_viaje(pk):
    hoy= date.today()
    todosLosViaje=Viaje.objects.filter(activo=True)
    for viaje in todosLosViaje:
        if viaje.fecha >= hoy:
            if viaje.ruta.combi.id == pk:
                return False
    return True

def no_se_encuentra_en_ruta(pk):
    queryset = Ruta.objects.filter(activo=True)
    for ruta in queryset:
        if ruta.combi.id == pk:
            return False
    return True

def se_encuentra_en_combi(pk):
    queryset = Combi.objects.filter(activo=True).values_list('chofer_id',flat=True)
    if pk in queryset:
        return True
    else:
        return False

def modificar_combi(request,pk):
    noModificado=False
    if(no_se_encuentra_en_viaje(pk)):
        choferRep=False
        modiTodo=True
        combi = Combi.objects.get(pk=pk)
        data = {'chofer':combi.chofer,'modelo':combi.modelo,'patente':combi.patente,'tipo':combi.tipo,'cantAsientos':combi.asientos}
        if request.method=="GET":
            form=FormCombi(data)
        else:
            form=FormCombi(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                choferRep=True if (se_encuentra_en_combi(d['chofer'].id)and ((d['chofer'].id) != combi.chofer.id)) else False
                modiTodo=True if (no_se_encuentra_en_ruta(pk)) else False
                validoPatente=[True if d['patente']==combi.patente else verificarPatente(d['patente']), verificarPatenteEnCombis(d['patente'])]
                if (not choferRep):
                    combi.chofer= d['chofer']
                    combi.tipo=d['tipo']
                    if modiTodo and validoPatente[0] and validoPatente[1]:
                        combi.modelo= d['modelo']
                        combi.asientos= d['cantAsientos']
                        combi.patente= d['patente']
                    else:
                        if combi.modelo != d['modelo'] or combi.asientos != d['cantAsientos'] or combi.patente != d['patente']:
                            return render(request,'demo1/modificar/formulario_modificar_combi.html',{"form":form,'choferRep':choferRep,'modiTodo':modiTodo, 'p1':validoPatente[0], 'p2': validoPatente[1]})
                    combi.save()
                    return redirect('listado_combi')
        return render(request,'demo1/modificar/formulario_modificar_combi.html',{"form":form,'choferRep':choferRep,'modiTodo':modiTodo, 'p1':True, 'p2':True})
    else:
        noModificado = True
        combis=filaDeCombi()
        page_obj,cantidad = listadoDePaginacion(combis, request)
        return render(request, 'demo1/listados/listado_combi.html', {'page_obj':page_obj, 'cantidad':cantidad, 'noModificado':noModificado})

def armarFilaViaje2(viajes):
    lista=[]
    for v in viajes:
        r=Ruta.objects.get(id=v.ruta.pk)
        combi=Combi.objects.get(id=r.combi.pk)
        o=Lugar.objects.get(id=r.origen.pk)
        d=Lugar.objects.get(id=r.destino.pk)
        tipo= 'Cama' if combi.tipo=='C' else 'Semicama'
        dic={'origen':o.nombre_de_lugar, 'destino':d.nombre_de_lugar,
            'hora': r.hora, 'cant': v.asientos, 'fecha':v.fecha, 'precio':v.precio, 'pk':v.pk, 'tipo':tipo}
        lista.append(dic)
    return lista 

def validarRutaEnviaje(ruta, da):
    o=Lugar.objects.get(id=ruta.origen.pk)
    d=Lugar.objects.get(id=ruta.destino.pk)
    if o.nombre_de_lugar.upper()==da['origen'].upper() and d.nombre_de_lugar.upper()== da['destino'].upper():
            return True
    return False

def buscarViajesPorRuta(d):
    viajes=Viaje.objects.filter(activo=True)
    lista=[]
    for i in viajes:
        if validarRutaEnviaje(i.ruta, d):
            lista.append(i)
    return lista

def buscarViajesEnLaBD(d):
    viajes=buscarViajesPorRuta(d)
    lista=[]
    if len(viajes)!=0:
        for i in viajes:
            if i.fecha >=date.today() and i.fecha>=d['fecha'] and i.asientos>0:
                if i.fecha==date.today():
                    if i.ruta.hora.hour >= datetime.now().hour:
                        lista.append(i)
                else:
                    lista.append(i)
    return lista

def buscarViajes(request):
    pasajero=buscar_pasajero(request.user.id)
    habilitado=pasajero.fecha_habilitacion <= date.today()
    
    validarOriyDes=False
    conViajes=None
    page_obj=[]
    fecha=False
    if request.method=='POST':
        form=FormoBusquedaViaje(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            validarOriyDes= d['origen'].upper()==d['destino'].upper()
            fecha=d['fecha']<date.today()
            if not validarOriyDes and not fecha:
                resultadoDeViajes=buscarViajesEnLaBD(d)
                if len(resultadoDeViajes)!=0:
                    conViajes=True
                    page_obj=armarFilaViaje2(viajes=resultadoDeViajes)  
                else:
                    conViajes=False                
    else:
        form=FormoBusquedaViaje()
    noHay=True if (conViajes!=None and not conViajes) else False
    return render(request,"demo1/form/formulario_viaje_busquedas.html", {'page_obj':page_obj, 'form': form, 'conViajes':conViajes, 'validarOriyDes':validarOriyDes, 'noHay':noHay, 'fecha':fecha,"habilitado":habilitado})

