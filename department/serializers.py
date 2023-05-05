from rest_framework import serializers
from core.models import department

class departmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    hod = serializers.CharField(required=True)
  
    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError('Dep. Name should be a string')
        return value

    def validate_hod(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError('HOD Name should be a string')
        return value

    class Meta:
        model = department
        fields = ['id', 'name', 'hod']