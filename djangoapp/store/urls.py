from django.urls import path
from .views import home,checkout,cart,updateItem,processOrder,register,lista_pedidos,detalhes_pedido
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

app_name = 'store'

urlpatterns = [
    # store:home
    path('', home, name="home"),

    # store:checkout
    path('checkout/', checkout, name="checkout"),

    # store:cart
    path('cart/', cart, name="cart"),

    #store:updateItem
    path('updateItem/', updateItem, name="updateItem"),

    #store:processOrder
    path('processOrder/', processOrder, name="processOrder"),

    #store:lista_pedidos
    path('pedidos/', lista_pedidos, name='lista_pedidos'),

    #store:lista_pedidos
    path('pedido/<int:id>/', detalhes_pedido, name='detalhes_pedido'),

    #store:login
    path('login/', CustomLoginView.as_view(template_name='store/login.html'), name='custom_login'),

    #store:logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #store:register
    path('register/', register, name='register'),


]
