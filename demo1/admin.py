from django.contrib import admin
from .models import Chofer
from .models import Pasajero
from .models import Tarjeta
from .models import Insumo
from .models import Lugar
from .models import Combi
from .models import Ruta
from .models import Viaje
from .models import Persona,Pasaje,CantInsumo

admin.site.register(Chofer)
admin.site.register(Pasajero)
admin.site.register(Tarjeta)
admin.site.register(Insumo)
admin.site.register(Lugar)
admin.site.register(Combi)
admin.site.register(Ruta)
admin.site.register(Viaje)
admin.site.register(Persona)
admin.site.register(CantInsumo)
admin.site.register(Pasaje)

