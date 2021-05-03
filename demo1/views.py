from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .forms import FormLugar, FormPasajero, FormLogin, FormChofer
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
    lugares=Lugar.objects.all()
    return render(request, 'demo1/listados/listado_lugar.html', {'lugares':lugares})

def listado_insumo(request):
    insumos=Insumo.objects.all()
    return render(request, 'demo1/listados/listado_insumo.html', {'insumos':insumos})

def listado_ruta(request):
    rutas=Ruta.objects.all()
    return render(request, 'demo1/listados/listado_ruta.html', {'rutas':rutas})

def listado_viaje(request):
    viajes=Viaje.objects.all()
    return render(request, 'demo1/listados/listado_viaje.html', {'viajes':viajes})

def lugar_new(request):
    if request.method == "POST":
        form = FormLugar(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            if datos['nombre']!='' and datos['provincia']!='':
                lugar = Lugar.objects.create()
                lugar.nombreYprovincia(datos['nombre'],datos['provincia'])
                lugar.save()
    else:
        form = FormLugar()
    return render(request, 'demo1/form/formulario_lugar.html', {'form': form})

def pasajero_new(request):
    if request.method=="POST":
        form=FormPasajero(request.POST)
        if form.is_valid():
            p=form.cleaned_data
            hoy=date.today()
            edad=hoy.year - p["fecha_de_nacimiento"].year
            edad-=((hoy.month,hoy.day)<(p["fecha_de_nacimiento"].month,p["fecha_de_nacimiento"].day))
            if edad>=18:
                usuario=User.objects.create(is_superuser=False,username=p["email"],password=p["password"],email=p["email"],first_name=p["first_name"],last_name=p["last_name"])
                pasajero=Pasajero.objects.create(usuario=usuario,dni=int(p["dni"]),telefono=int(p["telefono"]),tipo=p["tipo"],fecha_de_nacimiento=p["fecha_de_nacimiento"])
                pasajero.save()
    else:
        form=FormPasajero()
        edad=0
    return render(request,'demo1/form/formulario_usuario.html',{"form":form,"edad":edad})

def login_usuario(request):
    if request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=email,password=password)
            if user is not None:
                login(request, user)
                return redirect("http://127.0.0.1:8000/registrar/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = FormLogin()
    return render(request, "demo1/login.html", {"form":form})

def comparar_dni(unDni):
    dato=Chofer.objects.filter(dni=unDni)
    if dato.count()!= 0:
        return False
    return True

def comparar_email(unEmail):
    dato=Chofer.objects.filter(email=unEmail)
    if dato.count()!= 0:
        return False
    return True

def chofer_new(request):
    valor=False
    if request.method=="POST":
        form=FormChofer(request.POST)
        if form.is_valid():
            d=form.cleaned_data
            valor=comparar_dni(int(d['dni']))
            if valor:
                user= User.objects.create(email=d['email'], password=d['password'], first_name=d['first_name'], last_name=d['last_name'], is_staff=False)
                user.username=str(user.pk)+'pedroMartin'
                user.save()
                chofer= Chofer.objects.create(dni=int(d['dni']), telefono=d['telefono'], usuario=user)
                chofer.save()
                valor=False
            else:
                valor=True
    else:
        form=FormChofer()
    return render(request,'demo1/form/formulario_chofer.html',{"form":form, "valor":valor})

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

def detalle_lugar(request, pk):
    lugar = Lugar.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_lugar.html', {'lugar': lugar})

def detalle_tarjeta(request, pk):
    tarjeta = Tarjeta.objects.filter(pk=pk)
    return render(request, 'demo1/detalle/detalle_tarjeta.html', {'tarjeta': tarjeta})