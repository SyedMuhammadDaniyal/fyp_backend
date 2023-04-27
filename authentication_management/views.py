from django.db import IntegrityError, connection
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from authentication_management.serializers import RegisterSerializer, LoginSerializer
from authentication_management.utils.contant import LoginMessages
from core.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view 
from django.db import transaction



class RegisterUserAPIView(APIView):

  @transaction.atomic  
  def post(self, request):
    try:
      serialize = RegisterSerializer(data=request.data) 
      if serialize.is_valid():
          serialize.save()
          return Response(
              {
              "status": 200,
              "message": "Success",
              "body": {},
              "exception": None 
              }
          )
      else:
          return Response(
              {
              "status": 422,
              "message": serialize.errors,
              "body": {},
              "exception": "some exception" 
              }
          )
    except Exception as e:
      return Response(
            {
            "status": 400,
            "message": "Bad Request",
            "body": {},
            "exception": str(e)
            }
          )
        
    def delete(self, request, pk):
      try:
          instance = YourModel.objects.get(pk=pk)
      except YourModel.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
      instance.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)


class LoginUserApi(APIView):

  def post(self, request):
    serialize = LoginSerializer(data=request.data)
    
    if serialize.is_valid():
      try:
        user = User.objects.get(**serialize.validated_data)
        access_token = RefreshToken.for_user(user).access_token

        return Response(
          {
            "data": {
              "access_token": str(access_token)
            },
            "message": "Login Succes",
            "status": 200
          }
        )
      except:
        return Response(
          {
            "data": None,
            "message": LoginMessages.WRONG_CREDENTIALS.value,
            "status": 422
          }
        )
      
    return Response(
      {
        "data": serialize.errors,
        "message": None,
        "status": 422
      }
    )


@api_view(['GET'])
def getfyppanel(request):
  cursor = connection.cursor()
  sql = """ select core_fyppanel.id from core_fyppanel join core_user on core_fyppanel.user_id=core_user.id where core_user.email = :email"""
  cursor.execute(sql, {'email':'fypcord1@gmail.com'})    
  results = cursor.fetchall()
  return Response(results)
