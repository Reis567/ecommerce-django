import json
from .models import *

def cookieCart(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            print('New user')
            cart= {}


        print('Carrinho: ', cart)
        items = []
        pedido = {'get_cart_total':0,
                  'get_cart_items':0,
                  'shipping':False,
                  }
        itemsCarrinho = pedido['get_cart_items']

        for i in cart :
            try:
                print(cart[i])
                itemsCarrinho += cart[i]['quantidade']

                produto = Produto.objects.get(id=i)
                print(produto)
                total = (produto.price * cart[i]['quantidade'])

                pedido['get_cart_total'] += total
                pedido['get_cart_items'] += cart[i]['quantidade']

                item = {
                    'produto':{
                        'id':produto.id,
                        'nome':produto.nome,
                        'price':produto.price,
                        'foto':produto.foto.url
                    },
                    'quantidade':cart[i]['quantidade'],
                    'get_total':total
                }
                print(item)
                items.append(item)

                if produto.digital == False:
                    pedido['shipping'] = True
            except:
                print('Item nao existe')
    
        return {'itemsCarrinho':itemsCarrinho,'pedido':pedido, 'items':items }





