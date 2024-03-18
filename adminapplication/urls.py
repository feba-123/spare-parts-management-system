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
from adminapplication import views
from django.conf import settings
from django.conf.urls.static import static
app_name="adminapplication"

urlpatterns = [
        path('all_orders/', views.all_orders,name='all_orders'),
        path('adminhome/',views.admin_home, name='admin_home'),
        path('viewcat/',views.category_list, name='category_list'),
        path('viewitem/',views.item_list, name='item_list'),
        path('deadstock_item_list/', views.deadstock_item_list, name='deadstock_item_list'),
        path('addcat/',views.add_category, name='add_category'),
        path('add_item/', views.add_item, name='add_item'),
        path('edit_category/<int:category_id>/',views.edit_category, name='edit_category'),
        path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
        path('delete_category/<int:category_id>/',views.delete_category, name='delete_category'),
        path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
        path('delete_deadstock_item/<int:deadstock_item_id>/', views.delete_deadstock_item, name='delete_deadstock_item'),
        path('edit_deadstock_item/<int:deadstock_item_id>/', views.edit_deadstock_item, name='edit_deadstock_item'),
        path('add_deadstock_item/', views.add_deadstock_item, name='add_deadstock_item'),
        path('adminlogin/',views.Login_User, name='Login_User'),
        path('logout/', views.user_logout, name="user_logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)