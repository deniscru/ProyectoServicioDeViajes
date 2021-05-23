from django.db import models

class Persona(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    dni = models.IntegerField()
    telefono = models.BigIntegerField()
    activo = models.BooleanField(default=True)
        
    def __str__(self):
        return '%s %s' % (self.usuario.first_name, self.usuario.last_name)

class Chofer(Persona):
   pass

class Pasajero(Persona):
    TIPOS_PLANES = (
        ('B', 'Basic'),
        ('G', 'Gold'),)
    tipo = models.CharField(max_length=1, choices=TIPOS_PLANES)
    fecha_de_nacimiento = models.DateField()
    
class Tarjeta(models.Model):
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    numero = models.BigIntegerField()
    fecha_de_vencimiento = models.DateField()
    codigo = models.IntegerField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
         return '%s %s' % (self.pasajero.usuario.first_name, str(self.numero))

class Insumo(models.Model):
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)
    precio = models.FloatField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s %s' % (self.nombre, self.tipo)


class Lugar(models.Model):
    nombre_de_lugar = models.CharField(max_length=50)
    provincia = models.CharField(max_length=40)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s %s' % ('Localidad: '+self.nombre_de_lugar,', Provincia: '+self.provincia)

    def nombreYprovincia(self, unNombre, unaProvincia):
        self.nombre_de_lugar= unNombre
        self.provincia=unaProvincia

class Combi(models.Model):
    TIPOS_COMBI = (
        ('C', 'Cama'),
        ('S', 'Semicama'),
    )
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    patente = models.CharField(max_length=10)
    tipo = models.CharField(max_length=1, choices=TIPOS_COMBI)
    modelo = models.CharField(max_length=40)
    asientos = models.IntegerField()
    activo = models.BooleanField(default=True)
        
    def __str__(self):
        return '%s %s' % ('Modelo: '+self.modelo, ', Patente:'+self.patente)

class Ruta(models.Model):
    combi = models.ForeignKey(Combi, on_delete=models.CASCADE)
    origen = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='origen')
    destino = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='destino')
    hora = models.TimeField()
    distancia = models.IntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s %s' % ('Origen: '+self.origen.nombre_de_lugar,', Destino: '+self.destino.nombre_de_lugar, ', Hora: '+str(self.hora), ', Cant. de asientos de la combi:'+str(self.combi.asientos))

class Viaje(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    insumos = models.ManyToManyField(Insumo,blank=True)
    fecha = models.DateField()
    precio = models.FloatField()
    asientos = models.IntegerField()
    activo = models.BooleanField(default=True)
    vendidos= models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (str(self.ruta), str(self.fecha))
    
   



