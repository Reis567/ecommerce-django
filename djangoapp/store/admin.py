from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Pedido)
admin.site.register(Comprador)
admin.site.register(EnderecoEnvio)
admin.site.register(Produto)
admin.site.register(ItemdePedido)