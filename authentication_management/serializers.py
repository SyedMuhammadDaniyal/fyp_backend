from core.models import User, fyppanel
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  name = serializers.CharField(required=True)
  facultyid = serializers.CharField(required=True)
  designation = serializers.CharField(required=True)
  
  
  # class Meta:
  #   model = User
  #   fields = ('email', 'password', 'name')
    
  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['email'],
      name=validated_data['name'],
      password=validated_data['password'],
    )
    FYPPANEL = fyppanel.objects.create(
      user=user, 
      facultyid=validated_data['facultyid'],
      designation=validated_data['designation']
    )
    return user


class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()