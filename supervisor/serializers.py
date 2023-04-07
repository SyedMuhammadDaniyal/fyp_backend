from rest_framework import serializers

from core.models import supervisor

class supervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = supervisor
        # fields = '__all__'
        fields = ['id', 'name']