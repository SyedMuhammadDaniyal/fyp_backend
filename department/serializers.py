from rest_framework import serializers

from core.models import department

class departmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = department
        # fields = '__all__'
        fields = ['id', 'name']