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

from .views import SuperuserLogoutView,SuperuserLoginView,ItemAPIView,ItemDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    path('logout/', SuperuserLogoutView.as_view()),
    path('items/', ItemAPIView.as_view(), name='item-list-create'),
    path('itemsdetail/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]

