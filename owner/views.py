from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SuperuserLoginSerializer,ItemSerializer,CategorySerializer
from rest_framework_simplejwt.tokens import RefreshToken,BlacklistedToken
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Item,Category
from django.http import Http404
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Deadstock_Item
from .serializers import DeadstockItemSerializer


# class ItemAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         if request.user.is_superuser:
#           serializer = ItemSerializer(data=request.data)
#           if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#              return Response({"data": "not authenticated"})
#
#
#
#
# class ItemDetail(APIView):
#         authentication_classes = [JWTAuthentication]
#         permission_classes = [IsAuthenticated]
#         def get_object(self, pk):
#             try:
#                 return Item.objects.get(pk=pk)
#             except Item.DoesNotExist:
#                 raise Http404
#
#         def get(self, request, pk):
#             item = self.get_object(pk)
#             serializer = ItemSerializer(item)
#             return Response(serializer.data)
#
#         def put(self, request, pk, *args, **kwargs):
#           if request.user.is_superuser:
#             try:
#                 item = Item.objects.get(pk=pk)
#             except Item.DoesNotExist:
#                 raise Http404
#
#             serializer = ItemSerializer(item, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         def delete(self, request, pk):
#           if request.user.is_superuser:
#             item = self.get_object(pk)
#             item.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
          serializer = CategorySerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ItemAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data": "not authenticated"})

class ItemDetail(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        # if request.user.is_superuser:
            try:
                item = Item.objects.get(pk=pk)
            except Item.DoesNotExist:
                raise Http404

            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"data": "not authenticated"})

    def delete(self, request, pk, *args, **kwargs):
        if request.user.is_superuser:
            try:
                item = Item.objects.get(pk=pk)
            except Item.DoesNotExist:
                raise Http404

            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"data": "not authenticated"})

class DeadstockItemListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
            deadstock_items = Deadstock_Item.objects.all()
            serializer = DeadstockItemSerializer(deadstock_items, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
            serializer = DeadstockItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeadstockItemDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
            try:
                return Deadstock_Item.objects.get(pk=pk)
            except Deadstock_Item.DoesNotExist:
                raise Http404

    def get(self, request, pk, format=None):
            deadstock_item = self.get_object(pk)
            serializer = DeadstockItemSerializer(deadstock_item)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
            deadstock_item = self.get_object(pk)
            serializer = DeadstockItemSerializer(deadstock_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
            deadstock_item = self.get_object(pk)
            deadstock_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Deadstock_Item
from .serializers import BookingSerializer

class BookDeadstockItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id, format=None):
        quantity = int(request.data.get('quantity', 1))  # Convert quantity to integer
        address = request.data.get('address', '')
        notes = request.data.get('notes', '')

        try:
            item = Deadstock_Item.objects.get(pk=item_id)
        except Deadstock_Item.DoesNotExist:
            return Response({"error": "Deadstock item not found."}, status=status.HTTP_404_NOT_FOUND)

        if not item.available:
            return Response({"error": "Deadstock item is not available for booking."}, status=status.HTTP_400_BAD_REQUEST)

        if item.stock is not None and item.stock < quantity:
            return Response({"error": "Not enough stock available for booking."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = item.price * quantity  # Calculate total price

        booking_data = {
            'user': request.user.id,
            'item': item_id,
            'quantity': quantity,
            'address': address,
            'notes': notes,
        }
        if item.stock is not None:
            item.stock -= quantity
            item.save()
        serializer = BookingSerializer(data=booking_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)