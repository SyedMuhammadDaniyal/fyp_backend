from django.db import IntegrityError, connection
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from authentication_management.serializers import RegisterSerializer, LoginSerializer
from authentication_management.utils.contant import LoginMessages
from core.models import User, fyppanel
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from fyp_management.permission import IsSuperAdmin
from rest_framework.decorators import api_view 
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from google.auth import exceptions
from django.utils import timezone 
import random


class RegisterUserAPIView(APIView):
    permission_classes = [IsAuthenticated & IsSuperAdmin]

    @transaction.atomic  
    def post(self, request):
        try:
            serialize = RegisterSerializer(data=request.data) 
            if serialize.is_valid():
                serialize.save()

                subject = 'Registration'
                message = f'Your OTP is: \nPlease do not provide this OTP with Anyone.\nIt is a system-generated message. Please do not reply to this email.'
                email_from = request.user
                recipient_list = [email]

                try:
                    send_mail(subject, message, email_from, recipient_list)
                except exceptions.GoogleAuthError:
                    return Response({'error': 'Failed to send email.'}, status=500)
                return Response(
                    {
                    "status": 200,
                    "message": "PMO Registration successful.",
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
                if user.role == "fyp_panel":
                    fyp_panel = fyppanel.objects.get(user=user, deleted_at=None)
                    if fyp_panel.var == "unverified" or fyp_panel.var is None:
                        return Response({
                            "data": None,
                            "message": "Your Status is Unverified. Please contact your Admin.",
                            "status": "Success"
                        })

                force_upper_condition = True
                if force_upper_condition:
                    email = request.data.get('email')

                    # Generate an OTP
                    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

                    # Save the OTP in the user's session or database for verification later
                    user.otp = otp
                    user.is_active = True
                    user.save()

                    # Send the OTP to the user's email
                    subject = 'Registration OTP'
                    message = f'Your OTP is: {otp} \nPlease do not provide this OTP with Anyone.\nIt is a system-generated message. Please do not reply to this email.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]

                    try:
                        send_mail(subject, message, email_from, recipient_list)
                    except exceptions.GoogleAuthError:
                        return Response({'error': 'Failed to send email.'}, status=500)

                    return Response({
                        "data":[],
                        "message": "OTP successfully sent to your registered email.",
                        "status": 200
                    })
            except:
                return Response({
                    "data": None,
                    "message": LoginMessages.WRONG_CREDENTIALS.value,
                    "status": 422
                })
        return Response({
            "data": serialize.errors,
            "message": None,
            "status": 422
        })

class Validate_otpAPI(APIView):
    def patch(self, request):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')
            user = User.objects.get(email=email, deleted_at=None)
            s_otp = user.otp
            if str(otp) == user.otp:
                # OTP is valid, 
                user.last_login = timezone.now()
                user.save()
                
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "data": {
                        "access_token": access_token,
                        "id": user.id,
                        "name": user.name,
                        "role": user.role,
                        "dep_id": user.department.id,
                        "University_id":user.uni,
                    },
                    "message": "OTP validation successful. Access token generated.",
                    "status": 200
                })
            else:
                return Response({
                    "data": [],
                    "message": "Invalid OTP",
                    "status": 400
                })
        
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some errors",
                "body": {},
                "exception": str(e) 
                }
            )
