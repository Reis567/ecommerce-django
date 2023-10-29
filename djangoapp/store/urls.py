from django.urls import path
from .views import home,checkout,cart,updateItem,processOrder,register,lista_pedidos,detalhes_pedido,add_favorito, remove_favorito
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import FavoriteListView

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

    #store:detalhes_pedido
    path('pedido/<str:id_transacao>/', detalhes_pedido, name='detalhes_pedido'),

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

    #store:reset_password
    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),

    #store:password_reset_done
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),

    #store:password_reset_confirm
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),

    #store:password_reset_complete
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),

    


]

