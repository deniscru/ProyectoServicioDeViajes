from django import forms
from django.contrib.auth.models import User
from .models import Lugar, Pasajero, Chofer, Ruta, Insumo, Tarjeta, Combi, Persona
from datetime import date

class FormLugar(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, required=True)
    provincia= forms.CharField(label='Provincia', max_length=50, required=True)

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

class FormTarjeta(forms.Form):
    año=int(date.today().year)
    años=[]
    for i in range(año,(año+10)):
        años.append(i)
    numero=forms.CharField(required=True,max_length=18,min_length=14,label="Número Tarjeta")
    fecha_de_vencimiento=forms.DateField(required=True,label="Fecha Vencimiento",widget=forms.SelectDateWidget(years=años))
    codigo=forms.CharField(required=True,label="Código seguridad",min_length=3,max_length=4)


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

class FormCombiModi(forms.Form):
    TIPOS_COMBI = (
        ('C', 'Cama'),
        ('S', 'Semicama'),
    )
    chofer=forms.ModelChoiceField(queryset=Chofer.objects.filter(activo=True),label='choferes',widget=forms.Select())
    modelo=forms.CharField(required=True,max_length=50,label="Modelo")
    patente=forms.CharField(required=True,max_length=7,label="Patente")
    asientos= forms.CharField(required=True,max_length=2,label="Cantidad de asientos")
    tipo=forms.ChoiceField(widget=forms.RadioSelect, choices=TIPOS_COMBI)

def obtenerDatosDeInsumo():
        insumos= Insumo.objects.filter(activo=True).values()
        lista=[]
        for insumo in insumos:
            tupla=(insumo['id'], 'Nombre: '+insumo['nombre']+', Tipo: '+insumo['tipo'])
            lista.append(tupla)
        return lista

class FormViaje(forms.Form):
    def obtenerDatosDeRutas():
        rutas= Ruta.objects.filter(activo=True).values()
        lista=[]
        for ruta in rutas:
            combi=Combi.objects.filter(id=ruta['combi_id']).values()
            origen=Lugar.objects.filter(id=ruta['origen_id']).values()
            destino=Lugar.objects.filter(id=ruta['destino_id']).values()
            tupla=( ruta['id'] , 'Origen: '+origen[0]['nombre_de_lugar']+'; Destino: '+destino[0]['nombre_de_lugar']+'; Hora: '+ruta['hora'].isoformat()+'; Cant de Asientos de la combi: '+str(combi[0]['asientos']))
            lista.append(tupla)
        return lista

    datosDeRutas=obtenerDatosDeRutas()
    datosDeInsumos=obtenerDatosDeInsumo()
    ruta = forms.ChoiceField(choices=datosDeRutas, widget=forms.Select())
    insumo = forms.MultipleChoiceField(choices=datosDeInsumos, help_text='Para selecionar mas de una opcion maten precionado la tecla "ctrl"')
    años=[2021,2022]
    fecha = forms.DateField(required=True,label='Fecha',widget=forms.SelectDateWidget(years=años))
    precio = forms.FloatField(required=True,label="Precio")


class FormInsumo(forms.Form):
    tipo_insumo= ( ('dulse', 'DULSE'), ('salado', 'SALADO') )
    nombre = forms.CharField(required=True,max_length=70,label="Nombre del Producto")
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=tipo_insumo)
    precio = forms.FloatField(required=True, label='Precio')

class FormRuta(forms.Form):
    def obtenerCombi():
        combis= Combi.objects.filter(activo=True).values()
        lista=[]
        for combi in combis:
            tupla=(combi['id'], 'Modelo: '+combi['modelo']+'; Patente: '+combi['patente'])
            lista.append(tupla)
        return lista

    def obtenerLugar():
        lugares= Lugar.objects.filter(activo=True).values()
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
    distancia = forms.IntegerField(required=True,label="Distancia", max_value=1000)

class FormRutaModi(forms.Form):
    combi =forms.ModelChoiceField(queryset=Combi.objects.filter(activo=True),label='combis', widget=forms.Select())
    origen = forms.ModelChoiceField(queryset=Lugar.objects.filter(activo=True),label='Lugares',widget=forms.Select())
    destino = forms.ModelChoiceField(queryset=Lugar.objects.filter(activo=True),label='Lugares',widget=forms.Select())
    hora = forms.TimeField(required=True,label="Hora", widget=forms.TimeInput())
    distancia = forms.IntegerField(required=True,label="Distancia", max_value=50)

class FormViajeModi(forms.Form):
    datosDeInsumos=obtenerDatosDeInsumo()
    ruta = forms.ModelChoiceField(queryset=Ruta.objects.filter(activo=True),label='Rutas', widget=forms.Select())
    insumo = forms.MultipleChoiceField(choices=datosDeInsumos, help_text='Para selecionar mas de una opcion maten precionado la tecla "ctrl"')
    años=[2021,2022]
    fecha = forms.DateField(required=True,label='Fecha',widget=forms.SelectDateWidget(years=años))
    precio = forms.FloatField(required=True,label="Precio")
    asientos=forms.IntegerField(required=True,label="Asientos", help_text='Si va a modificar la cantida de asientos recuerde que no puede superar la capacidad maxima de la combi')


