from django.db import models


class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    grupos = models.ManyToManyField(Grupo, related_name='equipos', blank=True)

    def __str__(self):
        return self.nombre


class Partido(models.Model):
    fecha = models.DateTimeField()
    hora = models.TimeField(default='00:00:00')
    resultado = models.CharField(max_length=100)
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Competencia(models.Model):
    nombre = models.CharField(max_length=100)
    numero_grupos = models.IntegerField(default=0)
    grupos = models.ManyToManyField(Grupo)

    def __str__(self):
        return self.nombre
