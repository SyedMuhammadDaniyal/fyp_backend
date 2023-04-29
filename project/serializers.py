from core.models import project, department, supervisor
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class projectSerializer(serializers.ModelSerializer):
  title = serializers.CharField(required=True)
  year = serializers.CharField(required=True)
  batch = serializers.CharField(required=True)
  # grade = serializers.IntegerField(required=True)
  description = serializers.CharField(required=True)
  # status = serializers.CharField(required=True)
  domain = serializers.CharField(required=True)
  no_of_group_members = serializers.IntegerField(required=True)
  department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all())
  supervisor = serializers.PrimaryKeyRelatedField(queryset=supervisor.objects.all())

  class Meta:
    model = project
    fields = ['title', 'year', 'batch', 'description', 'status', 'domain', 'no_of_group_members', 'supervisor','department']    


class projectlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = '__all__'
        # fields = ['title']
