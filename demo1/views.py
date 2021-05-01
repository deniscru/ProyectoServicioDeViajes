from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Chofer
from .models import Pasajero
from .models import Tarjeta
from .models import Insumo
from .models import Lugar
from .models import Combi
from .models import Ruta
from .models import Viaje
from .models import Persona

def principal(request):
    administrador = User.objects.filter(is_superuser=True)
    choferes = Chofer.objects.all()
    Personas = Persona.objects.all()
    usuarios = User.objects.all()
    pasajeros = Pasajero.objects.all()
    tarjetas = Tarjeta.objects.all()
    combis = Combi.objects.all()
    Lugares = Chofer.objects.all()
    insumos = Insumo.objects.all()
    rutas = Ruta.objects.all()
    viajes = Viaje.objects.all()

    return render(request, 'demo1/principal.html', {'personas': Personas,'administrador': administrador, 'choferes': choferes, 'usuarios': usuarios, 'pasajeros': pasajeros, 'tarjetas': tarjetas, 'viajes': viajes, 'rutas': rutas, 'Lugares': Lugares, 'combis': combis, 'insumos': insumos})
