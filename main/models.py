from django.db import models
from django.conf import settings


class Ingredientes(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.count})"


class Alergenos(models.Model):
    name = models.CharField(max_length=100, unique=True)
    seleccionado = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Perfil(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    usernameSN = models.CharField(max_length=40)
    passwordSN = models.CharField(max_length=40)
    hashSN = models.CharField(max_length=40)
    listaAle = models.ManyToManyField(Alergenos, blank=True)
    listaIng = models.ManyToManyField(Ingredientes, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name




