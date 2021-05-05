from django import forms
from django.contrib.auth.models import User
from .models import Lugar, Pasajero, Chofer, Ruta, Insumo, Tarjeta
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

class FormCombi(forms.Form):
    def obtenerNombresDeChoferes():
        choferes=Chofer.objects.all().values()
        lista=[]
        for chofer in choferes:
            user=User.objects.filter(id=chofer['usuario_id']).values()
            tupla=( chofer['id'] , user[0]['first_name']+' '+user[0]['last_name'])
            lista.append(tupla)
        return lista

    TIPOS_COMBI = (
        ('C', 'Cama'),
        ('S', 'Semicama'),
    )
    choferes=Chofer.objects.all()
    nombreDeChoferes=obtenerNombresDeChoferes()
    chofer=forms.ChoiceField(widget=forms.Select(), choices=nombreDeChoferes)
    modelo=forms.CharField(required=True,max_length=50,label="Modelo")
    patente=forms.CharField(required=True,max_length=7,label="Patente")
    cantAsientos= forms.CharField(required=True,max_length=2,label="Cantidad de asientos")
    tipo=forms.ChoiceField(widget=forms.RadioSelect, choices=TIPOS_COMBI)

class FormViaje(forms.Form):
    def obtenerDatosDeRutas():
        rutas= Ruta.objects.all().values()
        lista=[]
        return lista
    
    def ontenerDatosDeInsumo():
        insumos= Insumo.objects.all().values()
        lista=[]
        return lista
    datosDeRutas=obtenerDatosDeRutas()
    ruta = forms.ChoiceField(widget=forms.Select(), choices=datosDeRutas)
    insumos = forms.ChoiceField(widget=forms.Select(), choices=datosDeRutas)
    años=[2021,2022]
    fecha = forms.DateField(required=True,label='Fecha',widget=forms.SelectDateWidget(years=años))
    precio = forms.CharField(required=True,max_length=10,label="Precio")
    asientosDisponible = forms.CharField(required=True,max_length=10,label="Asientos Disponibles")

class FormInsumo(forms.Form):
    def obtenerTarjeta():
        return None

    def obtenerPasajero():
        return None
    
    tipo_insumo= ( ('dulse', 'DULSE'), ('salado', 'SALADO') )
    tarjetas= obtenerTarjeta()
    pasajeros= obtenerPasajero()
    tarjeta = forms.ChoiceField(widget=forms.Select(), choices=[])
    pasajero = forms.ChoiceField(widget=forms.Select(), choices=[])
    nombre = forms.CharField(required=True,max_length=70,label="Nombre")
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_insumo)
    precio = forms.CharField(required=True,max_length=10,label="Precio")

class FormRuta(forms.Form):
    def obtenerCombi():
        return None
    def obtenerLugar():
        return None
    combi =forms.ChoiceField(widget=forms.Select(), choices=[])
    origen = forms.ChoiceField(widget=forms.Select(), choices=[])
    destino = forms.ChoiceField(widget=forms.Select(), choices=[])
    hora = forms.CharField(required=True,max_length=10,label="Hora")
    distancia = forms.CharField(required=True,max_length=10,label="Distancia")
