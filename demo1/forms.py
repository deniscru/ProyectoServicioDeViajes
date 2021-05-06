from django import forms
from django.contrib.auth.models import User
from .models import Lugar, Pasajero, Chofer, Ruta, Insumo, Tarjeta, Combi, Persona
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
    nombreDeChoferes=obtenerNombresDeChoferes()
    chofer=forms.ChoiceField(widget=forms.Select(), choices=nombreDeChoferes)
    modelo=forms.CharField(required=True,max_length=50,label="Modelo")
    patente=forms.CharField(required=True,max_length=7,label="Patente")
    cantAsientos= forms.CharField(required=True,max_length=2,label="Cantidad de asientos")
    tipo=forms.ChoiceField(widget=forms.RadioSelect, choices=TIPOS_COMBI)

class FormViaje(forms.Form):
    # error sobre la base de datos
    def obtenerDatosDeRutas():
        rutas= Ruta.objects.all().values()
        lista=[]
        for ruta in rutas:
            combi=Combi.objects.filter(id=ruta['combi_id']).values()
            origen=Lugar.objects.filter(id=ruta['origen_id']).values()
            destino=Lugar.objects.filter(id=ruta['destino_id']).values()
            tupla=( ruta['id'] , 'Origen: '+origen[0]['nombre_de_lugar']+' de '+origen[0]['provincia']+'; Destino: '+destino[0]['nombre_de_lugar']+' de '+destino[0]['provincia']+'; Hora: '+ruta['hora'].isoformat())
            lista.append(tupla)
        return lista
    
    def obtenerDatosDeInsumo():
        insumos= Insumo.objects.all().values()
        lista=[]
        for insumo in insumos:
            tupla=(insumo['id'], 'Nombre: '+insumo['nombre']+', Tipo: '+insumo['tipo'])
            lista.append(tupla)
        return lista

    datosDeRutas=obtenerDatosDeRutas()
    datosDeInsumos=obtenerDatosDeInsumo()
    ruta = forms.ChoiceField(choices=datosDeRutas, widget=forms.Select())
    insumo = forms.MultipleChoiceField(choices=datosDeInsumos)
    años=[2021,2022]
    fecha = forms.DateField(required=True,label='Fecha',widget=forms.SelectDateWidget(years=años))
    precio = forms.FloatField(required=True,label="Precio")
    asientosDisponible = forms.CharField(required=True,max_length=10,label="Asientos Disponibles")

class FormInsumo(forms.Form):
    #duda, el insumo siempre se paga con una tarjeta registrada?
    def obtenerTarjeta():
        tarjetas= Tarjeta.objects.all().values()
        lista=[]
        for t in tarjetas:
            tupla=(t['id'], 'Num° de Tarjeta: '+str(t['numero'])+'; Codigo: '+str(t['codigo']))
            lista.append(tupla)
        return lista

    def obtenerPasajero():
        pasajeros=Pasajero.objects.all().values()
        lista=[]
        for p in pasajeros:
            u=User.objects.filter(id=p['usuario_id']).values()
            tupla=(p['id'], 'Nombre: '+u[0]['first_name']+'; Apellido: '+u[0]['last_name']+'; DNI: '+str(p['dni']) )
            lista.append(tupla)
        return lista
    
    tipo_insumo= ( ('dulse', 'DULSE'), ('salado', 'SALADO') )
    tarjetas= obtenerTarjeta()
    pasajeros= obtenerPasajero()
    tarjeta = forms.ChoiceField(widget=forms.Select(), choices=tarjetas)
    pasajero = forms.ChoiceField(widget=forms.Select(), choices=pasajeros)
    nombre = forms.CharField(required=True,max_length=70,label="Nombre")
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_insumo)
    precio = forms.FloatField(required=True, label='Precio')

class FormRuta(forms.Form):
    def obtenerCombi():
        combis= Combi.objects.all().values()
        lista=[]
        for combi in combis:
            tupla=(combi['id'], 'Modelo: '+combi['modelo']+'; Patente: '+combi['patente'])
            lista.append(tupla)
        return lista

    def obtenerLugar():
        lugares= Lugar.objects.all().values()
        lista=[]
        for lugar in lugares:
            tupla=(lugar['id'], 'Localidad: '+lugar['nombre_de_lugar']+'; Provincia: '+lugar['provincia'])
            lista.append(tupla)
        return lista

    lugares=obtenerLugar()
    combis=obtenerCombi()
    combi =forms.ChoiceField(widget=forms.Select(), choices=combis)
    origen = forms.ChoiceField(widget=forms.Select(), choices=lugares)
    destino = forms.ChoiceField(widget=forms.Select(), choices=lugares)
    hora = forms.TimeField(required=True,label="Hora", widget=forms.TimeInput())
    distancia = forms.IntegerField(required=True,label="Distancia", max_value=50)
