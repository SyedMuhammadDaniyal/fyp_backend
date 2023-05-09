from core.models import notification, User
from rest_framework import serializers


class notificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    createdate = serializers.DateField(required=True)
    createtime = serializers.TimeField(required=True)
    createdby = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name = serializers.PrimaryKeyRelatedField(read_only = True, source='createdby.name')

    class Meta:
        model = notification
        fields = ['id','title', 'description', 'createdate', 'createtime', 'createdby','name']
