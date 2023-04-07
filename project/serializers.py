from core.models import project
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class projectSerializer(serializers.ModelSerializer):
  title = serializers.CharField(required=True)
  batch = serializers.CharField(required=True)
  # grade = serializers.IntegerField(required=True)
  description = serializers.CharField(required=True)
  # status = serializers.CharField(required=True)
  domain = serializers.CharField(required=True)
  


  class Meta:
    model = project
    # dep = project.objects.get()
    # fields = "__all__"
    fields = ['title', 'batch', 'description', 'domain', 'supervisor','department']    


class projectlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        # fields = '__all__'
        fields = ['title']