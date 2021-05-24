from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import FormLugar, FormCambiarContraseña,FormPasajeroModi, FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormTarjeta, FormoBusquedaViaje
from datetime import date, datetime
from django.core.paginator import Paginator
from .models import Chofer, Pasaje, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def change_password(request,pk):
    exito=False
    user=User.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormCambiarContraseña(request.POST)
        if form.is_valid():
            c=form.cleaned_data
            user.password=make_password(c['password'])
            user.save()
            exito=True
        return render(request, 'demo1/change_password.html', {'form': form,'exito':exito,'user':user})
    else:
        form = FormCambiarContraseña()
    return render(request, 'demo1/change_password.html', {'form': form,'exito':exito,'user':user})

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