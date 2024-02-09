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


from .views import add_to_cart,cart_api_view,cart_delete,reduce_cart_quantity,get_cart_list



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('add_to_cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart-api/', cart_api_view, name='cart-api'),
    path('delete/<int:b>/', cart_delete, name='cart-delete'),
    path('reduce_quantity/<int:b>/', reduce_cart_quantity, name='reduce-cart-quantity'),
    path('list/', get_cart_list, name='cart-list')
]

