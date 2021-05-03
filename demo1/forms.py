from django import forms

from .models import Lugar, Pasajero
from datetime import date

class FormLugar(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50)
    provincia= forms.CharField(label='Provincia', max_length=50)

class FormPasajero(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(1915,año):
        años.append(i)
    tipos=[("GOLD","GOLD"),("BASICO","BÁSICO")]
    email=forms.EmailField(required=True)
    dni=forms.CharField(required=True,label="Dni",max_length=8,min_length=8)
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    password = forms.CharField(required=True,label="Contraseña",min_length=6)
    telefono=forms.CharField(required=True,label="Teléfono",max_length=15)
    fecha_de_nacimiento = forms.DateField(required=True,label='Fecha Nacimiento',widget=forms.SelectDateWidget(years=años))
    tipo =forms.ChoiceField(widget=forms.RadioSelect, choices=tipos)

class FormLogin(forms.Form):
    email=forms.EmailField(required=True,label="Email")
    password=forms.CharField(required=True,widget=forms.PasswordInput,label="Contraseña")

class FormChofer(forms.Form):
    email=forms.EmailField(required=True)
    dni=forms.CharField(required=True,label="Dni", max_length=8,min_length=8)   
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    password = forms.CharField(required=True,label="Contraseña",min_length=6)
    telefono=forms.CharField(required=True,label="Teléfono",max_length=15)