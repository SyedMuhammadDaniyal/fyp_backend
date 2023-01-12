from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


class LoginUserApi(APIView):
  def post(self, request):
    serialize = LoginSerializer(data=request.data)
    
    if serialize.is_valid():
      return Response('logged in')
    
    return Response(
      serialize.errors
    )