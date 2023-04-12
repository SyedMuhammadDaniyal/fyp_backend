from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.models import supervisor, User, teamMember, department
from django.utils import timezone

class AddSupervisorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='user.name', required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all(), source='user.department')
    faculty_no = serializers.CharField(required=True)
    field_of_interest = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)

    class Meta:
        model = supervisor
        fields = ['id','email', 'password', 'name','faculty_no', 'field_of_interest', 'phone_no', 'department']

    def create(self, validated_data):
        sp = User.objects.create(
        email=validated_data['user']['email'],
        name=validated_data['user']['name'],
        password=validated_data['password'],
        department = validated_data['user']['department'],
        is_active = False,
        # updated_at = timezone.now
        )
        # department_id = validated_data.pop('department')
        # department_instance = department.objects.get(id=department_id)
        # project_id = validated_data.pop('project')
        # project_instance = project.objects.get(id=project_id)
        sup = supervisor.objects.create(
        user=sp, 
        faculty_no=validated_data['faculty_no'],
        field_of_interest=validated_data['field_of_interest'],
        phone_no=validated_data['phone_no'],
        # project =project_instance,        
        # department=department_instance,
        )
        return sup


class updateSupervisorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='user.name', read_only=True)
    faculty_no = serializers.CharField(required=True)
    field_of_interest = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)

    class Meta:
        model = supervisor
        fields = ['id','email', 'password', 'name','faculty_no', 'field_of_interest', 'phone_no']
