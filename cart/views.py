from django.shortcuts import render

from rest_framework import generics, status,permissions
from rest_framework.response import Response
from cart.models import Cart,Order_Items,Order
from owner.models import Item
from django.db import transaction
from rest_framework.views import APIView
from user.models import CustomUser

from rest_framework.permissions import IsAdminUser
from rest_framework import generics, permissions

from rest_framework import status
from .models import Cart, Item
from .serializers import CartSerializer,Order_ItemsSerializer,OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Cast
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Item
from owner.serializers import  ItemSerializer
from cart.serializers import BuyItemSerializer
class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, b):
        try:
            item = Item.objects.get(id=b)
            user = request.user
            cart = Cart.objects.get(user=user, item=item)
            if cart.quantity < cart.item.stock:
                cart.quantity += 1
                cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user, item=item, quantity=1)
            cart.save()

        return Response({'detail':"Item added to the cart"},status=status.HTTP_201_CREATED)


class CartRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, b):
        try:
            item = Item.objects.get(id=b)
            user = request.user
            cart = Cart.objects.filter(user=user, item=item).first()

            if cart:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart.delete()
            else:
                raise Cart.DoesNotExist

            return Response({"message": "Item removed from the cart."}, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"message": "Item not found in the cart."}, status=status.HTTP_404_NOT_FOUND)

class CartViewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).annotate(
            price_as_decimal=Cast('item__price', DecimalField()),
            subtotal=ExpressionWrapper(
                F('quantity') * F('price_as_decimal'),
                output_field=DecimalField()
            )
        )
        total = cart.aggregate(total=Sum('subtotal'))['total'] or 0

        # Serialize cart and include item details using ItemSerializer
        serialized_cart = CartSerializer(cart, many=True).data
        serialized_item_details = [ItemSerializer(item.item).data for item in cart]

        for cart_item, item_details in zip(serialized_cart, serialized_item_details):
            cart_item['item_details'] = item_details

        return Response({'cart': serialized_cart, 'total': total}, status=status.HTTP_200_OK)




class CartOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).annotate(
            price_as_decimal=Cast('item__price', DecimalField()),
            subtotal=ExpressionWrapper(
                F('quantity') * F('price_as_decimal'),
                output_field=DecimalField()
            )
        ).order_by('item__name')  # Order items by name, modify this as needed

        total = cart.aggregate(total=Sum('subtotal'))['total'] or 0

        # Serialize cart and include item details using ItemSerializer
        serialized_cart = CartSerializer(cart, many=True).data
        serialized_item_details = [ItemSerializer(item.item).data for item in cart]

        for cart_item, item_details in zip(serialized_cart, serialized_item_details):
            cart_item['item_details'] = item_details

        return Response({'cart': serialized_cart, 'total': total}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        address = request.data.get('address')  # Get address from request data
        notes = request.data.get('notes')      # Get notes from request data

        # Create Order object for each item in the cart
        cart = Cart.objects.filter(user=user)
        for cart_item in cart:
            Order.objects.create(
                item=cart_item.item,
                user=user,
                address=address,
                notes=notes
            )

        # Clear the cart after creating the order
        cart.delete()

        return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)
class CartDeleteAPIView(APIView):
    def delete(self, request, b):
        user = request.user
        item = get_object_or_404(Item, id=b)
        try:
            cart = Cart.objects.get(user=user, item=item)
            cart.delete()
            return Response({"message": "Item deleted from the cart."},status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"message": "Item not found in the cart."},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_cart_list(request):
    cart_items = Cart.objects.all()
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





class OrderItemsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            cart_entries = Cart.objects.filter(user=user)
            order=Order.objects.filter(user=user)
        except Cart.DoesNotExist or Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # order.delete()
        if not cart_entries:
            return Response({'detail': "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = request.data.get('address', '')
            notes = request.data.get('notes', '')

            for entry in cart_entries:
                entry.item.stock -= entry.quantity
                entry.item.save()
                order = Order.objects.create(
                    item=entry.item,
                    user=user,
                    address=address,
                    notes=notes,
                    quantity=entry.quantity,

                )
                order.save()

            cart_entries.delete()  # Delete cart entries after creating orders
            return Response({'detail': "Items ordered successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# class ViewOrdersAPIView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         orders = Order.objects.filter(user=request.user).annotate(
#             price_as_decimal=Cast('item__price', DecimalField()),
#             sub_total=ExpressionWrapper(F('quantity') * F('price_as_decimal'), output_field=DecimalField())
#         )
#         total = orders.aggregate(total=Sum('sub_total'))['total'] or 0
#         serializer = OrderSerializer(orders, many=True)
#         return Response({'order': serializer.data}, status=status.HTTP_200_OK)

class ViewOrdersAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all orders for the current user
        orders = Order.objects.filter(user=request.user).order_by('-id')

        # Serialize the orders data
        serializer = OrderSerializer(orders, many=True)

        # Return the serialized data in the response
        return Response({'orders': serializer.data}, status=status.HTTP_200_OK)


class BuyItemView(APIView):
    def post(self, request, item_id):
        serializer = BuyItemSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            address = serializer.validated_data['address']
            notes = serializer.validated_data['notes']
            try:
                item = Item.objects.get(pk=item_id)
            except Item.DoesNotExist:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

            if item.available and item.stock >= quantity:
                # Assuming you have a user authentication system in place, you can get the user who is buying the item
                user = request.user  # Assuming user is authenticated

                # Create an order
                order = Order.objects.create(
                    user=user,
                    item=item,
                    quantity=quantity,
                    address=address,
                    notes=notes
                )

                # Perform the purchase logic here, for example, deducting the stock, updating user's purchase history, etc.
                # You should implement this according to your application's logic

                # For example, deducting the stock:
                item.stock -= quantity
                item.save()

                return Response({"message": "Purchase successful", "order_id": order.pk}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Item not available or insufficient stock"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

