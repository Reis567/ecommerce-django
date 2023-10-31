from django.urls import path
from .views import home,checkout,cart,updateItem,processOrder,register,lista_pedidos,detalhes_pedido,add_favorito, remove_favorito
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import FavoriteListView
from .views import ProdutoDetailView

app_name = 'store'

urlpatterns = [
    # store:home
    path('', home, name="home"),

    #store:detalhes_produto/id
    path('produto/<int:pk>/', ProdutoDetailView.as_view(), name='detalhes_produto'),

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

    #store:detalhes_pedido
    path('pedido/<int:id>/', detalhes_pedido, name='detalhes_pedido'),

    #store:custom_login
    path('login/', CustomLoginView.as_view(template_name='store/login.html'), name='custom_login'),

    #store:logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #store:register
    path('register/', register, name='register'),

    #store:add_favorito
    path('add_favorito/', add_favorito, name='add_favorito'),

    #store:remove_favorito
    path('remove_favorito/', remove_favorito, name='remove_favorito'),

    #store:favoritos
    path('favoritos/',FavoriteListView.as_view(),name='favoritos'),


]

