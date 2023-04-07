from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.models import teamMember, User

class teamMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(required=True)
    rollno = serializers.CharField(required=True)
    grade = serializers.IntegerField(required=True)

    class Meta:
        model = teamMember
        # fields = '__all__'
        fields = ['email','password','name','rollno','grade']
    

    def create(self, validated_data):
        tm = User.objects.create(
        email=validated_data['email'],
        name=validated_data['name'],
        password=validated_data['password'],
        )
        team = teamMember.objects.create(
        user=tm, 
        rollno=validated_data['rollno'],
        grade=validated_data['grade'],
        )
        return tm
