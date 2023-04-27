from rest_framework import serializers
from .models import Sprint

class sprintSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sprint
        fields = ['id', 'project', 'milestone', 'title', 'start_date', 'end_date']