from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Lugar, Pasajero, Chofer, Ruta, Insumo, Tarjeta, Combi, Persona, Viaje , Pasaje
from datetime import date



class FormLugar(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, required=True)
    provincia= forms.CharField(label='Provincia', max_length=50, required=True)

class FormPasajero(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(1915,año):
        años.append(i)
    tipos=[("GOLD","Quiero ser Usuario GOLD"),("BASICO","Soy Usuario BÁSICO")]
    email=forms.EmailField(required=True)
    dni=forms.IntegerField(max_value=99999999,min_value=1000000,required=True,label="Dni")
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    password = forms.CharField(required=True,label="Contraseña",min_length=6)
    telefono=forms.IntegerField(required=True,label="Teléfono",max_value=1000000000000000000,min_value=100000)
    fecha_de_nacimiento = forms.DateField(required=True,label='Fecha Nacimiento',widget=forms.SelectDateWidget(years=años))
    tipo =forms.ChoiceField(widget=forms.RadioSelect, choices=tipos)

class FormCambiarContraseña(forms.Form):
    password = forms.CharField(required=True,label="Contraseña Nueva",min_length=6)

class FormPasajeroModi2(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(1915,año):
        años.append(i)
    tipos=[("GOLD","Quiero ser Usuario GOLD"),("BASICO","Soy Usuario BÁSICO")]
    email=forms.EmailField(required=True)
    dni=forms.IntegerField(max_value=99999999,min_value=1000000,required=True,label="Dni")
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    telefono=forms.IntegerField(required=True,label="Teléfono",max_value=1000000000000000000,min_value=100000)
    fecha_de_nacimiento = forms.DateField(required=True,label='Fecha Nacimiento',widget=forms.SelectDateWidget(years=años))
    tipo =forms.ChoiceField(widget=forms.RadioSelect, choices=tipos)

class FormPasajeroModi(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(1915,año):
        años.append(i)
    años1=[]
    for i in range(año,(año+10)):
        años1.append(i)
    tipos=[("GOLD","Soy usuario GOLD"),("BASICO","Quiero ser Usuario BÁSICO")]
    email=forms.EmailField(required=True)
    dni=forms.IntegerField(max_value=99999999,min_value=1000000,required=True,label="Dni")
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    telefono=forms.IntegerField(required=True,label="Teléfono",max_value=1000000000000000000,min_value=100000)
    fecha_de_nacimiento = forms.DateField(required=True,label='Fecha Nacimiento',widget=forms.SelectDateWidget(years=años))
    tipo =forms.ChoiceField(widget=forms.RadioSelect, choices=tipos)
    numero=forms.IntegerField(required=True,max_value=999999999999999999,min_value=100000000000000000,label="Número Tarjeta")
    fecha_de_vencimiento=forms.DateField(label="Fecha Vencimiento",widget=forms.SelectDateWidget(years=años1))
    codigo=forms.IntegerField(required=False,label="Codigo de Seguridad",min_value=100, max_value=999)

class FormTarjeta(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(año,(año+10)):
        años.append(i)
    numero=forms.IntegerField(required=True,max_value=999999999999999999,min_value=100000000000000000,label="Número Tarjeta")
    fecha_de_vencimiento=forms.DateField(required=True,label="Fecha Vencimiento",widget=forms.SelectDateWidget(years=años))
    codigo=forms.IntegerField(required=False,label="Codigo de Seguridad",min_value=100, max_value=999)

class FormLogin(forms.Form):
    email=forms.CharField(required=True,label="Email")
    password=forms.CharField(required=True,widget=forms.PasswordInput,label="Contraseña")

class FormChofer(forms.Form):
    email=forms.EmailField(required=True)
    dni=forms.IntegerField(max_value=99999999,min_value=1000000,required=True,label="Dni")  
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    password = forms.CharField(required=True,label="Contraseña",min_length=6)
    telefono=forms.IntegerField(required=True,label="Teléfono",max_value=1000000000000000000,min_value=100000)

class FormChoferModi(forms.Form):
    email=forms.EmailField(required=True)
    dni=forms.IntegerField(max_value=99999999,min_value=1000000,required=True,label="Dni")  
    first_name=forms.CharField(required=True,max_length=30,label="Nombre")
    last_name=forms.CharField(required=True,max_length=30,label="Apellido")
    password = forms.CharField(required=False, label="Contraseña",min_length=6)
    telefono=forms.IntegerField(required=True,label="Teléfono",max_value=1000000000000000000,min_value=100000)


class FormCombi(forms.Form):
    TIPOS_COMBI = (
        ('C', 'Cama'),
        ('S', 'Semicama'),
    )
    chofer=forms.ModelChoiceField(queryset=Chofer.objects.filter(activo=True),label='Choferes',widget=forms.Select())
    modelo=forms.CharField(required=True,max_length=50,label="Modelo")
    patente=forms.CharField(required=True,max_length=9,label="Patente")
    cantAsientos= forms.IntegerField(required=True,label="Cantidad de asientos")
    tipo=forms.ChoiceField(widget=forms.RadioSelect, choices=TIPOS_COMBI)

class FormViaje(forms.Form):
    mensaje='Debe ser menor o igual a la capacidad maxima de la combi (la capacidad maxima lo figura en la ruta seleccionada)'
    ruta = forms.ModelChoiceField(queryset=Ruta.objects.filter(activo=True),label='Rutas', widget=forms.Select())
    años=[2021,2022]
    fecha = forms.DateField(required=True,label='Fecha',widget=forms.SelectDateWidget(years=años))
    precio = forms.FloatField(required=True,label="Precio")
    asientos=forms.IntegerField(required=True,label="Cant. de Asientos Dis.", help_text=mensaje)

class FormInsumo(forms.Form):
    tipo_insumo= ( ('dulce', 'DULCE'), ('salado', 'SALADO') )
    nombre = forms.CharField(required=True,max_length=70,label="Nombre del Producto")
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_insumo)
    precio = forms.FloatField(required=True, label='Precio')

class FormRuta(forms.Form):
    combi =forms.ModelChoiceField(queryset=Combi.objects.filter(activo=True),label='Combis', widget=forms.Select())
    origen = forms.ModelChoiceField(queryset=Lugar.objects.filter(activo=True),label='Lugares origen',widget=forms.Select())
    destino = forms.ModelChoiceField(queryset=Lugar.objects.filter(activo=True),label='Lugares destino',widget=forms.Select())
    hora = forms.TimeField(required=True,label="Hora", widget=forms.TimeInput())
    distancia = forms.IntegerField(required=True,label="Distancia", max_value=1000)

class FormoBusquedaViaje(forms.Form):
    origen = forms.CharField(required=True,max_length=70,label="Origen")
    destino = forms.CharField(required=True,max_length=70,label="Destino")
    años=[2021,2022]
    fecha = forms.DateField(required=True,label='Fecha',widget=forms.SelectDateWidget(years=años))

class FormComentario(forms.Form):
    texto=forms.CharField(required=True,widget=forms.Textarea(attrs={"rows":5, "cols":100}),label="Comentario",max_length=500)



class FormPasaje(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(año,(año+10)):
        años.append(i)
    cantidad=forms.IntegerField(required=True,label="Cantidad de Pasajes",initial=1)
    numero=forms.IntegerField(required=True,max_value=999999999999999999,min_value=100000000000000000,label="Número Tarjeta")
    fecha_de_vencimiento=forms.DateField(required=True,label="Fecha Vencimiento",widget=forms.SelectDateWidget(years=años))
    codigo=forms.IntegerField(required=False,label="Codigo de Seguridad",min_value=100, max_value=999)
    insumos=forms.ModelChoiceField(queryset=Insumo.objects.filter(activo=True),required=False,label='Insumos')
    cantInsumo = forms.IntegerField(required=False,label="Cantidad",min_value=0)

class RegistroSintomas(forms.Form):
    tipo_eleccion= ( ('Si', True), ('No', False) )
    temperatura= forms.FloatField(required=True,max_value=42.0,min_value=35.0,label="Temperatura corporal",initial=36.5)
    tos=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    dolor_de_cabeza=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    falta_de_aire=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    diarrea=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    dolor_de_garganta=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    perdida_del_gusto=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    perdida_de_olfato=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
    dolor_en_el_pecho=forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_eleccion)
