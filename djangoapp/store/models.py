from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Comprador(models.model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    


class Produto(models.model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.nome

