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

from .views import ItemAPIView,ItemDetail,CategoryAPIView
from .views import DeadstockItemListCreateView, DeadstockItemDetailView,BookDeadstockItem
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoryAPIView.as_view(), name='categories-api'),
    path('items/', ItemAPIView.as_view(), name='item-list-create'),
    path('itemsdetail/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('deadstock_items/', DeadstockItemListCreateView.as_view(), name='deadstock-item-list-create'),
    path('deadstock_items/<int:pk>/', DeadstockItemDetailView.as_view(), name='deadstock-item-detail'),
    path('book/<int:item_id>/', BookDeadstockItem.as_view(), name='book_deadstock_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
