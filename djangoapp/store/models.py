from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Comprador(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Comprador"
        verbose_name_plural = "Compradores"
    


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    #foto = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

class Pedido(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.SET_NULL,null=True,blank=True )
    data_pedido = models.DateTimeField(auto_now_add=True)
    completo= models.BooleanField(default=False)
    id_transacao = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class ItemdePedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL,null=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)
    data_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedido"

class EnderecoEnvio(models.Model):
    comprador = models.ForeignKey(Comprador, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    endereco = models.CharField(max_length=200, null=False)
    cidade = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    cep = models.CharField(max_length=200, null=False)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endereco

    class Meta:
        verbose_name = "Endereço de Envio"
        verbose_name_plural = "Endereços de Envio"

