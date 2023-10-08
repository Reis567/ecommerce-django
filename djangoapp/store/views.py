from django.shortcuts import render

# Create your views here.
def home(request):
    context={}
    return render(
        request,
        'store/home.html',
        context
    )

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
