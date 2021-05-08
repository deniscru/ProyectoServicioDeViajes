from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import FormLugar, FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormRutaModi,FormTarjeta
from datetime import date

from .models import Chofer, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona

def principal(request):
    administrador = User.objects.filter(is_superuser=True)   
    return render(request, 'demo1/principal.html', {'administrador': administrador})

def detalle_usuario(request, pk):
    usuario = User.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_usuario.html', {'usuario': usuario})

def listado_chofer(request):
    choferes = Chofer.objects.all()
    return render(request, 'demo1/listados/listado_chofer.html', {'choferes':choferes})

def listado_persona(request):
    personas= Persona.objects.all()
    return render(request, 'demo1/listados/listado_persona.html', {'personas':personas})

def lisatdo_usuario(request):
    usuarios=User.objects.all()
    return render(request, 'demo1/listados/listado_usuario.html', {'usuarios':usuarios})

def lisatdo_pasajero(request):
    pasajeros=Pasajero.objects.all()
    return render(request, 'demo1/listados/listado_pasajero.html', {'pasajeros':pasajeros})

def listado_combi(request):
    combis=Combi.objects.all()
    return render(request, 'demo1/listados/listado_combi.html', {'combis':combis})

def listado_tarjeta(request):
    tarjetas=Tarjeta.objects.all()
    return render(request, 'demo1/listados/listado_tarjeta.html', {'tarjetas':tarjetas})

def listado_lugar(request):
    lugares=Lugar.objects.filter(activo=True)
    return render(request, 'demo1/listados/listado_lugar.html', {'lugares':lugares})

def listado_insumo(request):
    insumos=Insumo.objects.filter(activo=True)
    return render(request, 'demo1/listados/listado_insumo.html', {'insumos':insumos})

def listado_ruta(request):
    rutas=Ruta.objects.filter(activo=True)
    return render(request, 'demo1/listados/listado_ruta.html', {'rutas':rutas})

def listado_viaje(request):
    viajes=Viaje.objects.all()
    return render(request, 'demo1/listados/listado_viaje.html', {'viajes':viajes})

def compararLugar(d):
    lugares= Lugar.objects.all().values()
    for l in lugares:
        if l['nombre_de_lugar']==d['nombre'] and l['provincia']==d['provincia']:
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

def tarjeta_new(request):
    exitoso=False
    if request.method=="POST":
        form=FormTarjeta(request.POST)
        if form.is_valid():
            t=form.cleaned_data
            tarjeta=Tarjeta.objects.create(pasajero=Pasajero.objects.last(),numero=t["numero"],fecha_de_vencimiento=t["fecha_de_vencimiento"],codigo=t["codigo"],activo=True)
            tarjeta.save()
            exitoso=True
    else:
        form=FormTarjeta()
    return render(request,'demo1/form/formulario_tarjeta.html',{"form":form,"exitoso":exitoso}) 

def calcular_edad(p):
    hoy=date.today()
    edad=hoy.year - p["fecha_de_nacimiento"].year
    edad-=((hoy.month,hoy.day)<(p["fecha_de_nacimiento"].month,p["fecha_de_nacimiento"].day))
    return edad

def comparar_pasajero_dni(unDni):
    dato_chofer=Chofer.objects.filter(dni=unDni)
    dato_pasajero=Pasajero.objects.filter(dni=unDni)
    if dato_chofer.count()!= 0 and dato_pasajero.count()!=0:
        return False
    return True

def comparar_pasajero_email(unEmail):
    dato=User.objects.filter(email=unEmail)
    if dato.count()!=0:
        return False
    return True

def pasajero_new(request):
    exitoso=False
    fallido=False
    tipo=False
    edad=None
    if request.method=="POST":
        form=FormPasajero(request.POST)
        if form.is_valid():
            p=form.cleaned_data
            edad=calcular_edad(p)
            if edad>=18 and comparar_pasajero_dni(p["dni"]) and comparar_pasajero_email(p["email"]):
                usuario=User.objects.create(is_superuser=False,password=p["password"],email=p["email"],first_name=p["first_name"],last_name=p["last_name"])
                usuario.username=p["email"]
                usuario.save()
                pasajero=Pasajero.objects.create(usuario=usuario,dni=int(p["dni"]),telefono=int(p["telefono"]),tipo=p["tipo"],fecha_de_nacimiento=p["fecha_de_nacimiento"])
                pasajero.save()
                if (p["tipo"]=="BASICO"):
                    tipo=True
                else:
                   return redirect('http://127.0.0.1:8000/registrar/tarjeta/',pasajero)
                exitoso=True
            else:
                fallido=True
    else:
        form=FormPasajero()
    return render(request,'demo1/form/formulario_usuario.html',{"form":form,"edad":edad,"exitoso":exitoso,"fallido":fallido,"tipo":tipo}) 

def buscar_usuario(email,password):
    try:
        dato=User.objects.get(username=email,password=password) 
        return dato
    except:
        return None

def es_fallo_usuario(email):
    try:
        User.objects.get(username=email)
        return False
    except:
        return True

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
            user = buscar_usuario(email,password)
            if user is not None:
                login(request, user)
                if es_pasajero(user):
                    return redirect("http://127.0.0.1:8000/home_usuario/")
                elif es_admin(user):
                    return redirect("http://127.0.0.1:8000")
                else:
                    return redirect("http://127.0.0.1:8000/home_usuario/")
            elif es_fallo_usuario(email):
               fallo_usuario=True
            else:
                fallo_password=True
    else:
        form = FormLogin()
    return render(request, "demo1/login.html", {"form":form,"falloU":fallo_usuario,"falloP":fallo_password})

def home_usuario(request):
    return render(request,"demo1/home_usuario.html")

def logout_usuario(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/login/")

def comparar_dni(unDni):
    dato=Chofer.objects.filter(dni=unDni)
    if dato.count()!= 0:
        return False
    return True

def comparar_email(unEmail):
    dato=User.objects.filter(email=unEmail)
    if dato.count()!= 0:
        return False
    return True

def chofer_new(request):
    valor=False
    exitoso=False
    if request.method=="POST":
        form=FormChofer(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            if comparar_dni(int(d['dni'])) and comparar_email(d['email']):
                user= User.objects.create(email=d['email'], password=d['password'], first_name=d['first_name'], last_name=d['last_name'], is_staff=False)
                user.username=d['email']
                user.save()
                chofer= Chofer.objects.create(dni=int(d['dni']), telefono=d['telefono'], usuario=user)
                chofer.save()
                exitoso=True
            else:
                valor=True
    else:
        form=FormChofer()
    return render(request,'demo1/form/formulario_chofer.html',{"form":form, "valor":valor, "exitoso": exitoso})

def verficarChofer(idChofer):
    dato=Combi.objects.filter(chofer=idChofer)
    if dato.count()!= 0:
        return False
    return True

def combi_new(request):
    valor=False
    if request.method=='POST':
        form=FormCombi(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            if verficarChofer(d['chofer']):
                unChofer=Chofer.objects.get(id=d['chofer'])
                combi=Combi.objects.create(chofer=unChofer, modelo=d['modelo'], asientos=int(d['cantAsientos']), patente=d['patente'], tipo=d['tipo'])
                combi.save()
            else:
                valor=True
    else:
        form=FormCombi()
    return render(request, 'demo1/form/formulario_combi.html', {'form': form, 'valor': valor})

def verificarRuta(idRuta):
    dato=Viaje.objects.filter(ruta=idRuta)
    if dato.count()!= 0:
        return False
    return True

def viaje_new(request):
    valor=False
    if request.method=='POST':
        form=FormViaje(request.POST)
        if form.is_valid():
            d=form.cleaned_data  
            if verificarRuta(d['ruta']): 
                unaRuta=Ruta.objects.get(id=d['ruta'])  
                unosInsumos= Insumo.objects.filter(id__in= d['insumo'])       
                viaje=Viaje.objects.create(ruta=unaRuta, fecha=d['fecha'], precio=d['precio'], asientos=d['asientosDisponible'])
                viaje.insumos.set(unosInsumos)
                viaje.save()
            else:
                valor=True 
    else:
        form=FormViaje()
    return render(request, 'demo1/form/formulario_viaje.html', {'form': form, 'valor':valor})

def insumo_new(request):
    if request.method=='POST':
        form=FormInsumo(request.POST)
        if form.is_valid():
            d=form.cleaned_data   
            t=Tarjeta.objects.get(id=d['tarjeta'])
            p=Pasajero.objects.get(id=d['pasajero']) 
            insumo=Insumo.objects.create(tarjeta=t, pasajero=p, tipo=d['tipo'], nombre=d['nombre'],precio=d['precio'])
    else:
        form=FormInsumo()
    return render(request, 'demo1/form/formulario_insumo.html', {'form': form})

def ruta_new(request):
    if request.method=='POST':
        form=FormRuta(request.POST)
        if form.is_valid():
            d=form.cleaned_data 
            unOrigen=Lugar.objects.get(id=d['origen'])
            unDestino=Lugar.objects.get(id=d['destino'])
            unaCombi= Combi.objects.get(id=d['combi'])
            ruta=Ruta.objects.create(combi=unaCombi, origen=unOrigen, destino=unDestino, distancia=d['distancia'], hora=d['hora'])
            ruta.save()   
    else:
        form=FormRuta()
    return render(request, 'demo1/form/formulario_ruta.html', {'form': form})

def detalle_pasajero(request, pk):
    pasajero = Pasajero.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_pasajero.html', {'pasajero': pasajero})

def detalle_chofer(request, pk):
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
    ruta = Ruta.objects.get(pk=pk)
    if request.method=='POST':
        form=FormRutaModi(request.POST)
        if form.is_valid():
            d=form.cleaned_data 
            unOrigen=d['origen']
            unDestino=d['destino']
            unaCombi= d['combi']
            ruta.origen=unOrigen
            ruta.destino=unDestino
            ruta.combi=unaCombi
            ruta.hora= d['hora']
            ruta.distancia= d['distancia']
            ruta.save()   
    else:
        data = {'combi': ruta.combi,'origen': ruta.origen,'destino': ruta.destino,'hora': ruta.hora,'distancia': ruta.distancia}
        form=FormRutaModi(data)
    return render(request, 'demo1/modificar/formulario_modificar_ruta.html', {'form': form})

def modificar_insumo(request,pk):
    insumo = Insumo.objects.get(pk=pk)
    if request.method=='POST':
        form=FormInsumo(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            t=Tarjeta.objects.get(id=d['tarjeta'])
            p=Pasajero.objects.get(id=d['pasajero'])
            insumo.tarjeta = t
            insumo.pasajero = p
            insumo.tipo = d['tipo']
            insumo.nombre = d['nombre']
            insumo.precio = d['precio']
            insumo.save()
            
    else:
        data = {'tarjeta': insumo.tarjeta,'pasajero': insumo.pasajero,'tipo': insumo.tipo,'nombre': insumo.nombre,'precio': insumo.precio}
        form=FormInsumo(data)
    return render(request, 'demo1/modificar/formulario_modificar_insumo.html', {'form': form})

def detalle_lugar(request, pk):
    lugar = Lugar.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_lugar.html', {'lugar': lugar})

def modificar_lugar(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    if request.method == "POST":
        form = FormLugar(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            if datos['nombre']!='' and datos['provincia']!='':
                lugar.nombreYprovincia(datos['nombre'],datos['provincia'])
                lugar.save()
                
    else:
        data = {'nombre': lugar.nombre_de_lugar,'provincia': lugar.provincia}
        form = FormLugar(data)
    return render(request, 'demo1/modificar/formulario_modificar_lugar.html', {'form': form})

def eliminar_ruta(request, pk):
    ruta = Ruta.objects.get(pk=pk)
    ruta.activo = False
    ruta.save()
    rutas=Ruta.objects.filter(activo=True)
    return render(request, 'demo1/listados/listado_ruta.html', {'rutas':rutas})

def eliminar_insumo(request, pk):
    insumo = Insumo.objects.get(pk=pk)
    insumo.activo = False
    insumo.save()
    insumos=Insumo.objects.filter(activo=True)
    return render(request, 'demo1/listados/listado_insumo.html', {'insumos':insumos})

def eliminar_lugar(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    lugar.activo = False
    lugar.save()
    lugares=Lugar.objects.filter(activo=True)
    return render(request, 'demo1/listados/listado_lugar.html', {'lugares':lugares})
    

def detalle_tarjeta(request, pk):
    tarjeta = Tarjeta.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_tarjeta.html', {'tarjeta': tarjeta})