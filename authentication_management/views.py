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
from django.core.mail import send_mail
from django.conf import settings
from google.auth import exceptions
import random


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
            "message": "Registration successful.",
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


class LoginUserApi(APIView):
  def post(self, request):
    serialize = LoginSerializer(data=request.data)
    if serialize.is_valid():
      try:
        user = User.objects.get(**serialize.validated_data, deleted_at=None)
        
        email = request.data.get('email')
        
        # Generate an OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Save the OTP in the user's session or database for verification later

        # Send the OTP to the user's email
        subject = 'Registration OTP'
        message = f'Your OTP is: {otp} \nIt is system generated msg please donot reply to this email'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
    
        try:
          
          send_mail(subject, message, email_from, recipient_list)
          user  = User.objects.get(email=email, deleted_at=None)
          user.otp = otp
          user.is_active = True
          user.save()
          id = user.id
          name = user.name
          role = user.role
          dep = user.department.id
          access_token = RefreshToken.for_user(user).access_token
        except exceptions.GoogleAuthError:
          return Response({'error': 'Failed to send email.'}, status=500)
        return Response(
          {
            "data": {
              "access_token": str(access_token),
              "data":serialize.data,
              "id":id,
              "name":name,
              "role":role,
              "dep_id":dep
            },
            "message": "Login Succes. OTP sent to your email.",
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
