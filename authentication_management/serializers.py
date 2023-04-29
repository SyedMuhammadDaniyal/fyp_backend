from core.models import User, fyppanel, department
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True, source='user.email')
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  name = serializers.CharField(required=True, source='user.name')
  facultyid = serializers.CharField(required=True)
  designation = serializers.CharField(required=True)
  phoneno = serializers.CharField(required=True, source='user.phoneno')
  department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
  
  
  class Meta:
    model = User
    fields = ['email', 'password', 'name', 'phoneno', 'department']
    
  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['user']['email'],
      name=validated_data['user']['name'],
      password=validated_data['password'],
      phoneno=validated_data['user']['phoneno'],
      department=validated_data['user']['department'],
      role=User.PMO
    )
    FYPPANEL = fyppanel.objects.create(
      user=user, 
      facultyid=validated_data['facultyid'],
      designation=validated_data['designation']
    )
    return FYPPANEL


class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()