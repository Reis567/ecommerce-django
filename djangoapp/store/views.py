from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json
import datetime
import calendar
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .utils import *
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm

# Create your views here.
def home(request):
    categorias = Categoria.objects.all()
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
    else:
        cookieData = cookieCart(request)

        itemsCarrinho = cookieData['itemsCarrinho']
        pedido = cookieData['pedido']
        items = cookieData['items']
    
    categoria_selecionada = request.GET.get('categoria')
    if categoria_selecionada:
        categoria = Categoria.objects.get(id=categoria_selecionada)
        produtos = Produto.objects.filter(categoria=categoria)
    else:
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

    context = {
        'produtos': produtos,
        'itemsCarrinho': itemsCarrinho,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,  # Passar a categoria selecionada no contexto
    }
    return render(request, 'store/home.html', context)

def cart(request):

    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
    else:
        cookieData = cookieCart(request)

        itemsCarrinho = cookieData['itemsCarrinho']
        pedido = cookieData['pedido']
        items = cookieData['items']
        
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
        cookieData = cookieCart(request)

        itemsCarrinho = cookieData['itemsCarrinho']
        pedido = cookieData['pedido']
        items = cookieData['items']
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



def lista_pedidos(request):
    months_translation = {
        'January': 'Janeiro',
        'February': 'Fevereiro',
        'March': 'Março',
        'April': 'Abril',
        'May': 'Maio',
        'June': 'Junho',
        'July': 'Julho',
        'August': 'Agosto',
        'September': 'Setembro',
        'October': 'Outubro',
        'November': 'Novembro',
        'December': 'Dezembro',
    }
    
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedidos = Pedido.objects.filter(comprador=comprador)
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
        
        pedidos_info = []

        for pedido in pedidos:
            if pedido.completo  :
                cart_total = pedido.get_cart_total
                cart_items = pedido.get_cart_items
                month_name = pedido.data_pedido.strftime("%B")
                month_name_pt = months_translation.get(month_name, month_name)
                pedido_data = pedido.data_pedido.strftime("%d de ") + month_name_pt + pedido.data_pedido.strftime(" de %Y")
                
                # Acesse o primeiro item de pedido dentro do loop
                primeiro_item = pedido.itemdepedido_set.first()
                if primeiro_item:
                    foto_produto = primeiro_item.produto.foto
                else:
                    foto_produto = 'caminho_para_imagem_padrao.jpg'

                pedidos_info.append({
                    'pedido': pedido,
                    'cart_total': cart_total,
                    'cart_items': cart_items,
                    'pedido_data': pedido_data,
                    'foto_produto': foto_produto,
                })

        context = {
            'pedidos_info': pedidos_info,
            'items': items,
            'pedido': pedido,
            'itemsCarrinho': itemsCarrinho,
            'foto_produto': foto_produto,
        }
        return render(request, 'store/lista_pedidos.html', context)
    else:
        return redirect('store:custom_login')


def detalhes_pedido(request):
    context={}
    return render(request, 'store/detalhes_pedido.html', context)

def register(request):
    if request.user.is_authenticated:
        comprador = request.user.comprador
        pedido , created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
        items = pedido.itemdepedido_set.all()
        itemsCarrinho = pedido.get_cart_items
    else:
        cookieData = cookieCart(request)
        itemsCarrinho = cookieData['itemsCarrinho']
        pedido = cookieData['pedido']
        items = cookieData['items']

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:home')

    else:
        form = CustomUserCreationForm()

    context = {
        'items': items,
        'pedido': pedido,
        'itemsCarrinho': itemsCarrinho,
        'form': form,
    }
    return render(request, 'store/register.html', context)

class CustomLoginView(LoginView):  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            comprador = self.request.user.comprador
            pedido, created = Pedido.objects.get_or_create(comprador=comprador, completo=False)
            items = pedido.itemdepedido_set.all()
            itemsCarrinho = pedido.get_cart_items
        else:
            cookieData = cookieCart(self.request)

            itemsCarrinho = cookieData['itemsCarrinho']
            pedido = cookieData['pedido']
            items = cookieData['items']

        context['items'] = items
        context['pedido'] = pedido
        context['itemsCarrinho'] = itemsCarrinho

        return context
