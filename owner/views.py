from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SuperuserLoginSerializer,ItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken,BlacklistedToken
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Item
from django.http import Http404
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
class SuperuserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SuperuserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or user is not a superuser'},
                            status=status.HTTP_401_UNAUTHORIZED)


# logout admin(superuser)

class SuperuserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('hii')
        try:
            refresh_token = request.data.get("refresh_token")  # Use get() to avoid KeyError
            if not isinstance(refresh_token, str):
                raise ValueError("Refresh token must be a string")
            print('refresh_token:', refresh_token)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the token is already blacklisted
            if BlacklistedToken.objects.filter(token=refresh_token).exists():
                return Response({"detail": "Token is already blacklisted"}, status=status.HTTP_200_OK)

            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Superuser logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


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
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
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
          if request.user.is_superuser:
            try:
                item = Item.objects.get(pk=pk)
            except Item.DoesNotExist:
                raise Http404

            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
          if request.user.is_superuser:
            item = self.get_object(pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
