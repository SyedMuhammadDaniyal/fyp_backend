from rest_framework import serializers
from core.models import department

class departmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    hod = serializers.CharField(required=True)

    class Meta:
        model = department
        fields = ['id', 'name', 'hod']