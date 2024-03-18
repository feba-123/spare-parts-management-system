from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from owner.models import Category,Item,Deadstock_Item
from adminapplication.forms import CategoryForm
from django.contrib.auth.decorators import login_required
from cart.models import Order

@login_required
def admin_home(request):
    return render(request,'admin_home.html')

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'view_cat.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.FILES.get('category_image')
        Category.objects.create(category_name=category_name, category_image=category_image)
        return redirect('adminapplication:category_list')
    return render(request, 'add_cat.html')

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('adminapplication:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('adminapplication:category_list')
    return render(request, 'delete_category.html', {'category': category})


from django.shortcuts import render, redirect, get_object_or_404
from owner.models import Item
from adminapplication.forms import ItemForm,DeadstockItemForm  # Import your ItemForm
@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

@login_required
def add_item(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        available = request.POST.get('available') == 'on'
        category_id = request.POST.get('category')
        manufacturer = request.POST.get('manufacturer')
        item_image = request.FILES.get('item_image')

        # Create the item object
        item = Item.objects.create(
            item_name=item_name,
            price=price,
            description=description,
            stock=stock,
            available=available,
            category_id=category_id,
            manufacturer=manufacturer,
            item_image=item_image
        )

        return redirect('adminapplication:item_list')
    return render(request, 'add_item.html',{'categories':categories})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('adminapplication:item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item,'categories':categories})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('adminapplication:item_list')
    return render(request, 'delete_item.html', {'item': item})

@login_required
def deadstock_item_list(request):
    deadstock_items = Deadstock_Item.objects.all()
    return render(request, 'deadstock_item_list.html', {'deadstock_items': deadstock_items})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from owner.models import Deadstock_Item
from adminapplication.forms import DeadstockItemForm


@login_required
def edit_deadstock_item(request, deadstock_item_id):
    deadstock_item = get_object_or_404(Deadstock_Item, pk=deadstock_item_id)
    if request.method == 'POST':
        form = DeadstockItemForm(request.POST, request.FILES, instance=deadstock_item)
        if form.is_valid():
            form.save()
            return redirect('adminapplication:deadstock_item_list')
    else:
        form = DeadstockItemForm(instance=deadstock_item)
    return render(request, 'edit_deadstock_item.html', {'form': form, 'deadstock_item': deadstock_item})


@login_required
def delete_deadstock_item(request, deadstock_item_id):
    deadstock_item = get_object_or_404(Deadstock_Item, pk=deadstock_item_id)
    if request.method == 'POST':
        deadstock_item.delete()
        return redirect('adminapplication:deadstock_item_list')
    return render(request, 'delete_deadstock_item.html', {'deadstock_item': deadstock_item})


from django.shortcuts import render, redirect

@login_required
def add_deadstock_item(request):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        deadstock_item_name = request.POST.get('deadstock_item')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        available = request.POST.get('available') == 'on'
        manufacturer = request.POST.get('manufacturer')
        item_image = request.FILES.get('item_image')

        # Create the Deadstock_Item object
        deadstock_item = Deadstock_Item.objects.create(
            deadstock_item=deadstock_item_name,
            price=price,
            description=description,
            stock=stock,
            available=available,
            manufacturer=manufacturer,
            item_image=item_image
        )

        # Redirect to the deadstock item list page
        return redirect('adminapplication:deadstock_item_list')

    # Render the add deadstock item form template
    return render(request, 'add_deadstock_item.html')
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

def Login_User(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect('adminapplication:admin_home')
            else:
                return HttpResponseForbidden("Invalid login credentials or user not authorized.")
        else:
            return HttpResponseForbidden("Invalid login credentials.")
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('adminapplication:Login_User')

@login_required
def all_orders(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})