from rest_framework import serializers
from .models import Sprint
from core.models import project, milestone

class sprintSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    project = serializers.PrimaryKeyRelatedField(queryset=project.objects.all())
    milestone = serializers.PrimaryKeyRelatedField(queryset=milestone.objects.all())
    

    class Meta:
        model = Sprint
        fields = ['id', 'project', 'milestone', 'title', 'start_date', 'end_date']
