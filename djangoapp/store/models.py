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
    nome = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    #foto = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.nome

class Pedido(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.SET_NULL,null=True,blank=True )
    data_pedido = models.DateTimeField(auto_now_add=True)
    completo= models.BooleanField(default=False)
    id_transacao = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    