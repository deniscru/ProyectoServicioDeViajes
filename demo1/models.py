from django.db import models

class Persona(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    dni = models.IntegerField(unique=True)
    telefono = models.BigIntegerField()
        
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

    def registrar(self,un_email,un_dni,untelefono,un_first_name,un_last_name,una_fecha,una_password,un_tipo):
        self.email=un_email
        self.dni=int(un_dni)
        self.telefono=int(untelefono)
        self.first_name=un_first_name
        self.last_name=un_last_name
        self.password=una_password
        self.tipo=un_tipo  
    
class Tarjeta(models.Model):
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    numero = models.BigIntegerField(unique=True)
    fecha_de_vencimiento = models.DateField()
    codigo = models.IntegerField()
    
    def __str__(self):
         return '%s %s' % (self.pasajero.usuario.first_name, str(self.numero))

class Insumo(models.Model):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)
    precio = models.FloatField()
    
    def __str__(self):
        return '%s %s' % (self.nombre, self.pasajero.usuario.first_name)


class Lugar(models.Model):
    nombre_de_lugar = models.CharField(max_length=50)
    provincia = models.CharField(max_length=40)
    
    def __str__(self):
        return '%s %s' % (self.nombre_de_lugar, self.provincia)

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
        
    def __str__(self):
        return '%s %s' % (self.patente, self.chofer.usuario.first_name)

class Ruta(models.Model):
    combi = models.ForeignKey(Combi, on_delete=models.CASCADE)
    origen = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='origen')
    destino = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='destino')
    hora = models.TimeField()
    distancia = models.IntegerField()

    def __str__(self):
        return '%s %s %s' % (self.origen.nombre_de_lugar, self.destino.nombre_de_lugar, str(self.hora))

class Viaje(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    insumos = models.ManyToManyField(Insumo)
    fecha = models.DateField()
    precio = models.FloatField()
    asientos = models.IntegerField()
    
    def __str__(self):
        return '%s %s' % (str(self.ruta), str(self.fecha))
    
    class Meta:
        unique_together = ('ruta', 'fecha',)



