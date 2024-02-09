from django.shortcuts import render

from rest_framework import generics, status,permissions
from rest_framework.response import Response
from cart.models import Cart
from owner.models import Item
from .serializers import CartSerializer
from rest_framework.views import APIView
from user.models import CustomUser

from rest_framework.permissions import IsAdminUser
from rest_framework import generics, permissions

from rest_framework import status
from .models import Cart, Item
from .serializers import CartSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.shortcuts import get_object_or_404







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    quantity = request.data.get('quantity', 1)

    try:
        cart = Cart.objects.get(user=user, item=item)
        available_quantity = item.stock - cart.quantity

        # Convert quantity and available_quantity to integers
        quantity = int(quantity)
        available_quantity = int(available_quantity)

        if quantity <= available_quantity:
            cart.quantity += quantity
            cart.save()
        else:
            return Response({'error': 'Requested quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)

    except Cart.DoesNotExist:
        quantity = int(quantity)
        if quantity <= item.stock:
            # Convert quantity to an integer before creating the Cart object
            cart = Cart.objects.create(user=user, item=item, quantity=int(quantity))
            cart.save()
        else:
            return Response({'error': 'Requested quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_api_view(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    serializer = CartSerializer(cart_items, many=True)

    total = 0

    for item in cart_items:
        try:
            item_quantity = int(item.quantity)
            item_price = float(item.item.price)
            total += item_quantity * item_price
        except (ValueError, TypeError):
            # Handle conversion errors gracefully
            pass

    response_data = {
        'cart': serializer.data,
        'total': total
    }

    return Response(response_data, status=status.HTTP_200_OK)





@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_delete(request, b):
    user = request.user
    item = get_object_or_404(Item, id=b)

    try:
        cart = Cart.objects.get(user=user, item=item)
        cart.delete()
        return Response({'detail': 'Item removed from the cart'}, status=status.HTTP_204_NO_CONTENT)
    except Cart.DoesNotExist:
        return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)


# views.py



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])


def reduce_cart_quantity(request, b):
    user = request.user
    item = get_object_or_404(Item, id=b)

    try:
        cart = Cart.objects.get(user=user, item=item)

        # Get the quantity to reduce from the request data (default to 1)
        quantity_to_reduce = int(request.data.get('quantity', 1))

        # Ensure that the quantity to reduce is a positive integer
        if quantity_to_reduce <= 0:
            return Response({'error': 'Invalid quantity to reduce'}, status=status.HTTP_400_BAD_REQUEST)

        # Reduce the cart quantity
        cart.reduce_quantity(quantity_to_reduce)

        return Response({'detail': 'Item quantity reduced in the cart'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_cart_list(request):
    cart_items = Cart.objects.all()
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

