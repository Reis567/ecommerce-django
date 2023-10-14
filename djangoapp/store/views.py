from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



# Create your views here.
def home(request):
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

    context = {'produtos': produtos}

    return render(request, 'store/home.html', context)

def cart(request):
    context={}
    return render(
        request,
        'store/cart.html',
        context
    )


def checkout(request):
    context={}
    return render(
        request,
        'store/checkout.html',
        context
    )
