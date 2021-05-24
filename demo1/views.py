from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import FormLugar,FormPasajeroModi, FormPasajeroModi2,FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormTarjeta, FormoBusquedaViaje ,FormComentario
from datetime import date, datetime
from django.core.paginator import Paginator
from .models import Chofer, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona,Comentario
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import datetime
from .views2 import change_password, consultarPasajesUserPendi, consultarPasajesUserCance



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

def listado_chofer(request):
    choferes= obtenerChoferes() 
    paginator= Paginator(choferes, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_chofer.html', {'page_obj':page_obj, 'cantidad':cantidad})

def listado_persona(request):
    personas= Persona.objects.all()
    return render(request, 'demo1/listados/listado_persona.html', {'personas':personas})

def lisatdo_usuario(request):
    usuarios=User.objects.all()
    return render(request, 'demo1/listados/listado_usuario.html', {'usuarios':usuarios})

def lisatdo_pasajero(request):
    pasajeros=Pasajero.objects.all()
    return render(request, 'demo1/listados/listado_pasajero.html', {'pasajeros':pasajeros})

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
    paginator= Paginator(combis, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_combi.html', {'page_obj':page_obj, 'cantidad':cantidad, 'noSePuede':False})

def listado_tarjeta(request):
    tarjetas=Tarjeta.objects.all()
    return render(request, 'demo1/listados/listado_tarjeta.html', {'tarjetas':tarjetas})

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
    paginator= Paginator(lugares, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_lugar.html', {'page_obj':page_obj, 'cantidad':cantidad})

def verificarInsumoEnViaje(pk):
    hoy= datetime.date.today()
    viajes=Viaje.objects.filter(activo=True)
    for i in viajes:
        if i.fecha >= hoy:
            insumos=i.insumos.values()
            for j in insumos:
                if j['id']==pk:
                    return False
    return True

def obtenerInsumosLista():
    insumos=Insumo.objects.filter(activo=True).values()
    lista=[]
    for i in insumos:
        dato=verificarInsumoEnViaje(i['id'])
        dic={'nombre':i['nombre'], 'tipo':i['tipo'], 'precio':i['precio'], 'dato':dato , 'pk':i['id']}
        lista.append(dic)
    return lista

def listado_insumo(request):
    insumos=obtenerInsumosLista()
    paginator= Paginator(insumos, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_insumo.html',{'page_obj':page_obj, 'cantidad':cantidad, 'noSeElimina':False})

def verficarRuta2(pk):
        viajes=Viaje.objects.filter(activo=True).values()
        ruta = Ruta.objects.filter(pk=pk).values()
        for v in viajes:
            if ruta[0]['id']==v['ruta_id'] and v['fecha']>=date.today():
                return False
        return True

def obtenerOrigenesDestino():
    rutas=Ruta.objects.filter(activo=True).values()
    lista=[]
    for r in rutas:
        h=verficarRuta2(int(r['id']))
        o=Lugar.objects.filter(id=r['origen_id']).values()
        d=Lugar.objects.filter(id=r['destino_id']).values()
        dic={'origen': o[0]['nombre_de_lugar']+', '+o[0]['provincia'], 'destino': d[0]['nombre_de_lugar']+', '+d[0]['provincia'], 'hora':r['hora'], 'pk':r['id'], 'sePuede':h }
        lista.append(dic)
    return lista

def listado_ruta(request):
    rutas=obtenerOrigenesDestino()
    paginator= Paginator(rutas, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_ruta.html',{'page_obj':page_obj, 'cantidad':cantidad})

def armarFilaViaje(viajes=Viaje.objects.filter(activo=True).values()):
    lista=[]
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
    paginator= Paginator(viajes, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_viaje.html', {'page_obj':page_obj, 'cantidad':cantidad})

def compararLugar(d):
    lugares= Lugar.objects.filter(activo=True).values()
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

def tarjeta_new(request):
    exitoso=False
    fecha_vencimiento_no_es_valida=False
    if request.method=="POST":
        form=FormTarjeta(request.POST)
        if form.is_valid():
            p=FormTarjeta.get_pasajero()
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
            else:
                fecha_vencimiento_no_es_valida=True
    else:
        form=FormTarjeta()
    return render(request,'demo1/form/formulario_tarjeta.html',{"form":form,"exitoso":exitoso,"fv":fecha_vencimiento_no_es_valida}) 

def tarjeta_new_modificado(request):
    exitoso=False
    fecha_vencimiento_no_es_valida=False
    tarjetaRep=False
    p=FormTarjeta.get_pasajero()
    pasajero= buscar_pasajero_dni(p["dni"])
    login(request, pasajero.usuario)
    tiene= tiene_tarjeta(pasajero.pk)
    if request.method=="POST":
        form=FormTarjeta(request.POST)
        if form.is_valid():
            t=form.cleaned_data
            if tiene:
                tarj= obtener_tarjeta(pasajero.pk)
                tarjetaRep= tarjetaRepetidaModificado(tarj.pk,t["numero"])
            else:
                tarjetaRep= tarjetaRepetida(t["numero"])
            if fecha_vencimiento_es_valida(t["fecha_de_vencimiento"]):
                if not tarjetaRep:
                    if tiene and tarj.numero == int(t["numero"]):
                        tarjeta=tarj
                    else:
                        tarjeta=Tarjeta.objects.create(pasajero=pasajero,numero=t["numero"],fecha_de_vencimiento=t["fecha_de_vencimiento"],codigo=t["codigo"],activo=True)
                    pasajero.tipo=p["tipo"]
                    pasajero.save()
                    tarjeta.save()
                    exitoso=True
            else:
                fecha_vencimiento_no_es_valida=True
    else:
        if tiene:
            tarj= obtener_tarjeta(pasajero.pk)
            data={'numero':tarj.numero,'codigo':tarj.codigo,'fecha_de_vencimiento':tarj.fecha_de_vencimiento}
            form=FormTarjeta(data)
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
                    t=FormTarjeta()
                    t.change_pasajero(p)
                    return redirect("http://127.0.0.1:8000/registrar_tarjeta/")
            else:
                fallido=True
    else:
        form=FormPasajero()
    return render(request,'demo1/form/formulario_usuario.html',{"form":form,"edad":edad,"exitoso":exitoso,"tipo":tipo,"dniUnico":dniUnico,"mailUnico":mailUnico,"fallido":fallido}) 

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
                        t=FormTarjeta()
                        t.change_pasajero(p)
                        return redirect("http://127.0.0.1:8000/registrar_tarjeta_modificado/")
            
        return render(request,'demo1/modificar/formulario_modificar_pasajero.html',{"form":form,'pk':pk,"edad":edad,"exitoso":exitoso,"dniUnico":dniUnico,"mailUnico":mailUnico})
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
                   
                        if not tarjetaRepetidaModificado(tarjeta.pk,p["numero"]):
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
                            else:
                                vencNoValida=True
                        else:
                            tarjetaRep=True
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

def home_usuario(request):
    return render(request,"demo1/home_usuario.html")

def home_usuario_chofer(request):
    return render(request,"demo1/home_usuario_chofer.html")

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
            print(mailUnico, dniUnico)
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
    dato=Combi.objects.filter(chofer=idChofer.pk)
    if dato.count()!= 0:
        return False
    return True

def verificarPatenteEnCombis(unaPatente):
    combi=Combi.objects.filter(patente=unaPatente)
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

def verificarFechaYRuta(unaFecha, ruta):
    return not Viaje.objects.filter(activo=True).filter(fecha=unaFecha).filter(ruta=ruta.pk).exists()

def verifivarAsientos(d):
    ruta2=Ruta.objects.get(id=d['ruta'].pk)
    unaCombi=Combi.objects.get(id=ruta2.combi.pk)
    if d['asientos'] <=unaCombi.asientos:
        return True
    else:
        return False

def viaje_new(request):
    valor=False
    exitoso=False
    asientosValidos=False
    if request.method=='POST':
        form=FormViaje(request.POST)
        if form.is_valid():
            d=form.cleaned_data  
            a=verificarFechaYRuta(d['fecha'], d['ruta'])
            v=verifivarAsientos(d)
            if a and v:
                unaRuta=Ruta.objects.get(id=d['ruta'].pk)  
                #unosInsumos= Insumo.objects.filter(id__in= d['insumo'])       
                viaje=Viaje.objects.create(ruta=unaRuta, fecha=d['fecha'], precio=d['precio'], asientos= d['asientos'],activo=True)
                #viaje.insumos.set(unosInsumos)
                viaje.save()
                exitoso=True
            if not a:
                valor=True 
            if not v:
                asientosValidos=True
    else:
        form=FormViaje()
    return render(request, 'demo1/form/formulario_viaje.html', {'form': form, 'valor':valor, 'exitoso':exitoso, 'asientosValidos':asientosValidos})

def verificarInsumo(datos):
    insumos=Insumo.objects.all().values()
    for i in insumos:
        if i['nombre'].upper()==datos['nombre'].upper():
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

def verficarRuta(d):
    rutas=Ruta.objects.all()
    for r in rutas:
        if r.combi==d['combi'] or r.origen==d['origen'] and r.destino==d['destino'] and r.distancia==d['distancia'] and r.hora==d['hora']:
            return False
    return True

def ruta_new(request):
    exitoso=False
    desOriEquls=False
    rutaRep = False
    if request.method=='POST':
        form=FormRuta(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            desOriEquls= d['origen'].pk == d['destino'].pk
            rutaRep = Ruta.objects.filter(origen = d['origen'].pk).filter(destino = d['destino'].pk).filter(hora = d['hora']).exists()
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


def comentario_new(request):
    exitoso=False
    if request.method=="POST":
        form=FormComentario(request.POST)
        if form.is_valid():
            c=form.cleaned_data
            pasajero=buscar_pasajero(request.user.id)
            comentario=Comentario.objects.create(texto=c["texto"],pasajero=pasajero,viaje=c["viaje"])
            comentario.save()
            exitoso=True
    else:
        form=FormComentario()
    return render(request,'demo1/form/formulario_comentario.html',{'form':form,'exitoso':exitoso})


def detalle_pasajero(request, pk):
    pasajero = Pasajero.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_pasajero.html', {'pasajero': pasajero})

def detalle_chofer(request, pk):
    print('detalle ',pk)
    chofer = Chofer.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_chofer.html', {'chofer': chofer})

def detalle_combi(request, pk):
    combi = Combi.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_combi.html', {'combi': combi})

def detalle_viaje(request, pk):
    viaje = Viaje.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_viaje.html', {'viaje': viaje})

def detalle_insumo(request, pk):
    insumo = Insumo.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_insumo.html', {'insumo': insumo})

def detalle_ruta(request, pk):
    ruta = Ruta.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_ruta.html', {'ruta': ruta})

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
                rutaRep = Ruta.objects.exclude(pk=pk).filter(origen = unOrigen).filter(destino = unDestino).filter(hora = d['hora']).exists()
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
        paginator= Paginator(rutas, 10)
        cantidad=False if (paginator.count == 0) else True 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'demo1/listados/listado_ruta.html',{'page_obj':page_obj, 'cantidad':cantidad, 'noModificado':noModificado})

def modificar_insumo(request,pk):
    noModificado=False
    if verificarInsumoEnViaje(pk):
        insumo = Insumo.objects.get(pk=pk)
        if request.method=='POST':
            form=FormInsumo(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                insumo.tipo = d['tipo']
                insumo.nombre = d['nombre']
                insumo.precio = d['precio']
                insumo.save()
                return redirect('listado_insumo') 
        else:
            data = {'tipo': insumo.tipo,'nombre': insumo.nombre,'precio': insumo.precio}
            form=FormInsumo(data)
        return render(request, 'demo1/modificar/formulario_modificar_insumo.html', {'form': form})
    else:
        noModificado=True
        insumos=obtenerInsumosLista()
        paginator= Paginator(insumos, 10)
        cantidad=False if (paginator.count == 0) else True 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
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
                if datos['nombre']!='' and datos['provincia']!='':
                    lugar.nombreYprovincia(datos['nombre'],datos['provincia'])
                    lugar.save()
                    return redirect('listado_lugar')
        else:
            data = {'nombre': lugar.nombre_de_lugar,'provincia': lugar.provincia}
            form = FormLugar(data)
        return render(request, 'demo1/modificar/formulario_modificar_lugar.html', {'form': form})
    else:
        noModificado=True
        lugares=obtenerListaDeLugares()
        paginator= Paginator(lugares, 10)
        cantidad=False if (paginator.count == 0) else True 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
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
    user= obtenerChoferes() 
    paginator= Paginator(user, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_chofer.html', {'page_obj':page_obj, 'cantidad':cantidad,"noEliminado":noEliminado})

def eliminar_combi(request, pk):
    noEliminado=False
    if no_se_encuentra_en_ruta(pk):
        combi = Combi.objects.get(pk=pk)
        combi.activo = False
        combi.save()
    else:
        noEliminado=True
    combis=filaDeCombi()
    paginator= Paginator(combis, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_combi.html', {'page_obj':page_obj, 'cantidad':cantidad, 'noEliminado':noEliminado})

def eliminar_viaje(request, pk):
    viaje = Viaje.objects.get(pk=pk)
    exitoso=True
    if no_tieneViajesVendidos(pk):
        viaje.activo = False
        viaje.save()
        exitoso=False
    viajes=armarFilaViaje()
    paginator= Paginator(viajes, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_viaje.html', {'page_obj':page_obj, 'cantidad':cantidad, 'exitoso':exitoso})

def eliminar_ruta(request, pk):
    exitosoE=True
    if verficarRuta2(pk):
        ruta = Ruta.objects.get(pk=pk)
        ruta.activo = False
        ruta.save()
        exitosoE=False
    rutas=obtenerOrigenesDestino()
    paginator= Paginator(rutas, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  
    return render(request, 'demo1/listados/listado_ruta.html',{'page_obj':page_obj, 'cantidad':cantidad, 'exitosoE':exitosoE})

def eliminar_insumo(request, pk):
    noSeElimina=False
    if verificarInsumoEnViaje(pk):
        insumo = Insumo.objects.get(pk=pk)
        insumo.activo = False
        insumo.save()
    else:
        noSeElimina=True
    insumos=Insumo.objects.filter(activo=True)
    paginator= Paginator(insumos, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_insumo.html',{'page_obj':page_obj, 'cantidad':cantidad, 'noSeElimina':noSeElimina})

def eliminar_lugar(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    fallido=False
    if obtenerValorUnLugar(lugar.id):
        lugar.activo = False
        lugar.save()
    else:
        fallido=True
    lugares=Lugar.objects.filter(activo=True)
    paginator= Paginator(lugares, 10)
    cantidad=False if (paginator.count == 0) else True 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'demo1/listados/listado_lugar.html', {'page_obj':page_obj, 'cantidad':cantidad,"fallido":fallido})
   
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
            form=FormChofer(data)
        else:
            form=FormChofer(request.POST)
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
        paginator= Paginator(user, 10)
        cantidad=False if (paginator.count == 0) else True 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'demo1/listados/listado_chofer.html', {'page_obj':page_obj, 'cantidad':cantidad,"noModificado":noModificado})

def no_tieneViajesVendidos(pk):
    return Viaje.objects.get(pk=pk).vendidos == 0 

def modificar_viaje(request,pk):
    viaje= Viaje.objects.get(pk=pk)
    asientosValidos=True
    viajeValido=True
    noModificado=False
    if no_tieneViajesVendidos(pk):
        data= {'ruta':viaje.ruta,'fecha':viaje.fecha,'precio':viaje.precio,'asientos':viaje.asientos}
        if request.method=='GET':
            form=FormViaje(data)
        else:
            form=FormViaje(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                viajeValido=verificarFechaYRuta(d['fecha'], d['ruta'])
                asientosValidos= viaje.ruta.combi.asientos >= d['asientos']
                if viajeValido and asientosValidos:
                    #unosInsumos= Insumo.objects.filter(id__in= d['insumo'])       
                    #viaje.insumos.set(unosInsumos)
                    viaje.ruta=d['ruta']
                    viaje.fecha=d['fecha']
                    viaje.precio= d['precio']
                    viaje.asientos=d['asientos']
                    viaje.save()
                    return redirect('listado_viaje') 
        return render(request, 'demo1/modificar/formulario_modificar_viaje.html', {'form': form, 'asientosValidos':asientosValidos,'viajeValido':viajeValido,'capacidad':str(viaje.ruta.combi.asientos)}) 
    else:
        noModificado=True
        viajes=armarFilaViaje()
        paginator= Paginator(viajes, 10)
        cantidad=False if (paginator.count == 0) else True 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'demo1/listados/listado_viaje.html', {'page_obj':page_obj, 'cantidad':cantidad,'noModificado':noModificado})

def no_se_encuentra_en_viaje(pk):
    hoy= datetime.date.today()
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
        paginator= Paginator(combis, 10)
        cantidad=False if (paginator.count == 0) else True 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
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
    if len(viajes)!=0:
        lista=[]
        for i in viajes:
            if i.fecha >=date.today() and i.asientos>0:
                if i.fecha==date.today():
                    if i.ruta.hora.hour >= datetime.now().hour:
                        lista.append(i)
                else:
                    lista.append(i)
        return lista
    return None

def buscarViajes(request):
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
                if resultadoDeViajes!=None:
                    conViajes=True
                    page_obj=armarFilaViaje2(viajes=resultadoDeViajes)  
                else:
                    conViajes=False                
    else:
        form=FormoBusquedaViaje()
    noHay=True if (conViajes!=None and not conViajes) else False
    return render(request,"demo1/form/formulario_viaje_busquedas.html", {'page_obj':page_obj, 'form': form, 'conViajes':conViajes, 'validarOriyDes':validarOriyDes, 'noHay':noHay, 'fecha':fecha})

