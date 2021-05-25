from django.db.models.fields import BLANK_CHOICE_DASH
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import FormLugar,FormPasaje, FormCambiarContraseña,FormPasajeroModi, FormPasajero, FormLogin, FormChofer, FormCombi, FormViaje, FormInsumo, FormRuta,FormTarjeta, FormoBusquedaViaje
from datetime import date, datetime
from django.core.paginator import Paginator
from .models import Chofer, Pasajero, Tarjeta, Insumo, Lugar, Combi, Ruta, Viaje, Persona
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import datetime
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

def comprar_pasaje(request,pk):
    compro=False
    cantInsumos={}
    FormPasaje().change_cantInsumos(cantInsumos)
    pasaje={}
    pasajero = buscar_pasajero(request.user.pk)
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
                if p['cantInsumo'] > 0 and p['insumos'] !=None:
                    hayInsumosSelec=True
                    cantInsumos[str(p['insumos'].nombre)]= p['cantInsumo']
                    for key in cantInsumos:
                        pasaje['precio']=pasaje['precio'] + (Insumo.objects.filter(nombre=key)[0].precio * cantInsumos[key])
                    FormPasaje().change_cantInsumos(cantInsumos)

    else:
        form = FormPasaje()
    return render(request, 'demo1/comprar_pasaje.html', {'form': form,'hayPasajes':hayPasajes,'viaje':viaje,'cantInsumos':cantInsumos,'pasaje':pasaje,'hayPasajesSelec':hayPasajesSelec,'hayInsumosSelec':hayInsumosSelec,'compro':compro})

def sumar_al_pasaje(request,pk):
    compro=False
    cantInsumos=FormPasaje().get_cantInsumos()
    pasaje={}
    pasajero = buscar_pasajero(request.user.pk)
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
                if p['cantInsumo'] > 0 and p['insumos'] !=None:
                    hayInsumosSelec=True
                    cantInsumos[str(p['insumos'].nombre)]= p['cantInsumo']
                    for key in cantInsumos:
                        pasaje['precio']=pasaje['precio'] + (Insumo.objects.filter(nombre=key)[0].precio * cantInsumos[key])
                    FormPasaje().change_cantInsumos(cantInsumos)

    else:
        form = FormPasaje()
    return render(request, 'demo1/comprar_pasaje.html', {'form': form,'hayPasajes':hayPasajes,'viaje':viaje,'cantInsumos':cantInsumos,'pasaje':pasaje,'hayPasajesSelec':hayPasajesSelec,'hayInsumosSelec':hayInsumosSelec,'compro':compro})








