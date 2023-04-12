from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.models import teamMember, User, department

class teamMemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='user.name', required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
    rollno = serializers.CharField(required=True)
    seatno = serializers.CharField(required=True)
    enrollmentno = serializers.CharField(required=True)
    phoneno = serializers.CharField(required=True)
    
    class Meta:
        model = teamMember
        fields = ['email','password','name','rollno', 'seatno', 'enrollmentno', 'phoneno', 'department']
    
    def create(self, validated_data):
        tm = User.objects.create(
        email=validated_data['user']['email'],
        name=validated_data['user']['name'],
        password=validated_data['password'],
        department = validated_data['user']['department'],
        is_active = False
        )
        # department_id = validated_data.pop('department')
        # department_instance = department.objects.get(id=department_id)
        # project_id = validated_data.pop('project')
        # project_instance = project.objects.get(id=project_id)
        team = teamMember.objects.create(
        user=tm, 
        rollno=validated_data['rollno'],
        seatno=validated_data['seatno'],
        enrollmentno=validated_data['enrollmentno'],
        phoneno=validated_data['phoneno'],
        # project =project_instance,        
        # department=department_instance,
        )
        return team

# class studentlistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = teamMember
#         fields = '__all__'

class updateStudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='user.name', read_only=True)
    department = serializers.PrimaryKeyRelatedField(source='user.department', read_only=True)
    rollno = serializers.CharField(required=True)
    seatno = serializers.CharField(required=True)
    enrollmentno = serializers.CharField(required=True)
    phoneno = serializers.CharField(required=True)

    class Meta:
        model = teamMember
        fields = ['id','email', 'password', 'name','rollno', 'seatno', 'enrollmentno', 'phoneno', 'department']
