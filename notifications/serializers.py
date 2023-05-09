from core.models import notification, fyppanel
from rest_framework import serializers


class notificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    createdate = serializers.DateField(required=True)
    createtime = serializers.TimeField(required=True)
    createdby = serializers.PrimaryKeyRelatedField(read_only = True, source='createdby.user.name')

    class Meta:
        model = notification
        fields = ['title', 'description', 'createdate', 'createtime', 'createdby']    
