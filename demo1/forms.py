from django import forms

from .models import Lugar
from .models import Pasajero
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
    telefono=forms.CharField(required=True,label="Teléfono",max_length=15)
    nombre=forms.CharField(required=True,max_length=30,label="Nombre")
    apellido=forms.CharField(required=True,max_length=30,label="Apellido")
    fecha_de_nacimiento = forms.DateField(required=True,label='Fecha Nacimiento',widget=forms.SelectDateWidget(years=años))
    password = forms.CharField(required=True,label="Contraseña",min_length=6)
    tipo =forms.ChoiceField(widget=forms.RadioSelect, choices=tipos)