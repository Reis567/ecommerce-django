from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_total':0,
                  'get_cart_items':0,
                  'shipping':False,
                  }
        itemsCarrinho = pedido['get_cart_items']
    produtos = Produto.objects.all()

    produtos_por_pagina = 6

    paginator = Paginator(produtos, produtos_por_pagina)

    # Obtenha o número da página a partir dos parâmetros da solicitação
    page = request.GET.get('page')

    try:
        # Obtenha a página atual
        produtos = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um número inteiro, exiba a primeira página
        produtos = paginator.page(1)
    except EmptyPage:
        # Se a página estiver vazia (for maior que o número total de páginas), exiba a última página
        produtos = paginator.page(paginator.num_pages)

    context = {'produtos': produtos,
               'itemsCarrinho':itemsCarrinho,}

    return render(request, 'store/home.html', context)

def cart(request):

    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
    else:
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
            print(cart[i])
            itemsCarrinho += cart[i]['quantidade']
        
    context={'items':items,
             'pedido':pedido ,
            'itemsCarrinho':itemsCarrinho,}
    return render(
        request,
        'store/cart.html',
        context
    )

@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_total':0,
                  'get_cart_items':0,
                  'shipping':False,
                  }
        itemsCarrinho = pedido['get_cart_items']
    context={'items':items,
             'pedido':pedido ,
            'itemsCarrinho':itemsCarrinho,}
    return render(
        request,
        'store/checkout.html',
        context
    )


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productId)

    comprador = request.user.comprador
    produto = Produto.objects.get(id=productId)
    pedido, created = Pedido.objects.get_or_create(comprador=comprador, completo=False)

    itemdePedido, created = ItemdePedido.objects.get_or_create(pedido=pedido, produto=produto)

    if action == 'add':
        itemdePedido.quantidade = (itemdePedido.quantidade + 1)
    elif action == 'remove':
        itemdePedido.quantidade = (itemdePedido.quantidade - 1)

    itemdePedido.save()
    print('feito')

    if itemdePedido.quantidade <= 0:
        itemdePedido.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido, created = Pedido.objects.get_or_create(comprador=comprador, completo=False)

        total_str = data['user']['total'].replace(',', '.')
        total = float(total_str)
        pedido.transaction_id = transaction_id

        # Define uma margem de tolerância para a comparação de números de ponto flutuante
        tolerance = 0.001  # Ajuste esse valor conforme necessário

        # Converte pedido.get_cart_total para float
        cart_total = float(pedido.get_cart_total)

        if abs(total - cart_total) < tolerance:
            pedido.completo = True
        else:
            print(cart_total)
        pedido.save()

        if pedido.shipping == True:
            EnderecoEnvio.objects.create(
                comprador = comprador,
                pedido=pedido,
                endereco=data['shipping']['endereco'],
                cidade=data['shipping']['cidade'],
                estado=data['shipping']['estado'],
                cep=data['shipping']['cep'],
            )
        

    else:
        print('Usuário não logado')
    print(request.body)
    return JsonResponse('Payment done', safe=False)