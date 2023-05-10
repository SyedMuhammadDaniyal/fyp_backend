from core.models import notification, User, department
from rest_framework import serializers
from datetime import datetime


class notificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    createdate = serializers.DateField(default = datetime.now().date())
    createtime = serializers.TimeField(default = datetime.now().strftime('%H:%M'))
    createdby = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=department.objects.all())
    name = serializers.PrimaryKeyRelatedField(read_only = True, source='createdby.name')

    class Meta:
        model = notification
        fields = ['id','title', 'description', 'createdate', 'createtime', 'department','createdby','name']
