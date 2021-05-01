from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import FormLugar
from .forms import FormPasajero
from datetime import date

from .models import Chofer, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona

def principal(request):
    administrador = User.objects.filter(is_superuser=True)   
    return render(request, 'demo1/principal.html', {'administrador': administrador})

def detalle_usuario(request, pk):
    usuario = User.objects.filter(pk=pk)
    return render(request, 'demo1/detalle_usuario.html', {'usuario': usuario})

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
    return render(request, 'demo1/listados/listado_pasajero.html', {'combis':combis})

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
    return render(request, 'demo1/formulario.html', {'form': form})

def pasajero_new(request):
    if request.method=="POST":
        form=FormPasajero(request.POST)
        if form.is_valid():
            p=form.cleaned_data
            hoy=date.today()
            edad=hoy.year - p["fecha_de_nacimiento"].year
            edad-=((hoy.month,hoy.day)<(p["fecha_de_nacimiento"].month,p["fecha_de_nacimiento"].day))
            if edad>=18:
                pasajero=Pasajero.objects.create()
                pasajero.registrar(p["email"],p["dni"],p["telefono"],p["first_name"],p["last_name"],p["fecha_de_nacimiento"],p["password"],p["tipo"])
                pasajero.save()
    else:
        form=FormPasajero()
        edad=18
    return render(request,'demo1/formulario_usuario.html',{"form":form,"edad":edad})