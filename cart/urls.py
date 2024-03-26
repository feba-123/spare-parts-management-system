"""
URL configuration for spare_part_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


# from .views import add_to_cart,cart_api_view,cart_delete,reduce_cart_quantity,get_cart_list,AddOrder,order_items
from .views import  AddToCartAPIView,CartRemoveAPIView,CartViewAPIView,CartDeleteAPIView,get_cart_list,ViewOrdersAPIView,OrderItemsAPIView,BuyItemView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('add_to_cart/', AddToCartView.as_view(), name='add-to-cart'),
    # path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    # path('cart-api/', cart_api_view, name='cart-api'),
    # path('delete/<int:b>/', cart_delete, name='cart-delete'),
    # path('reduce_quantity/<int:b>/', reduce_cart_quantity, name='reduce-cart-quantity'),
    # path('list/', get_cart_list, name='cart-list'),
    path('add-to-cart/<int:b>/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('cart-remove/<int:b>/', CartRemoveAPIView.as_view(), name='cart_remove'),
    path('cart-view/', CartViewAPIView.as_view(), name='cart_view'),
    path('cart-delete/<int:b>/', CartDeleteAPIView.as_view(), name='cart_delete'),
    path('list/', get_cart_list, name='cart-list'),
    # path('orderitems/<int:id>/',AddOrder,name='order_items'),
    # path('order/<int:id>/',order_items),
    # path('CartOrderAPIView/', CartOrderAPIView.as_view(), name='CartOrderAPIView'),
    path('api/order-items/', OrderItemsAPIView.as_view(), name='order_items_api'),
    path('view-orders/', ViewOrdersAPIView.as_view(), name='view_orders'),
    path('buy/<int:item_id>/', BuyItemView.as_view(), name='buy_item'),
]

