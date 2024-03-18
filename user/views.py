from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework import status,generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout, authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated

class Register_user(APIView):


    def post(self, requset):
        register_serilizer =  UserSerializer(data=requset.data)
        if  register_serilizer.is_valid():
             register_serilizer.save()
             return Response( register_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(register_serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims or user information here
#         # Example: token['username'] = user.username
#         return token
# class LoginView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

class UserLoginAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer =UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                serialized_user = UserSerializer(user)
                return Response({
                    'user': serialized_user.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'status': f"{user.username} logged in successfully",
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class registered_users(APIView):
   permission_classes = [IsAuthenticated]
   def get(self, request):
        if request.user.is_superuser:
          user= CustomUser.objects.all()
          user_serilizer =UserSerializer(user, many=True)
          return Response( user_serilizer.data)
        else:
            return Response({'error':'auth not provided'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

