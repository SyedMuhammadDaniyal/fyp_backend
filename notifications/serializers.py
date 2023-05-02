from core.models import notification, fyppanel
# from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class notificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    # isactive = serializers.BooleanField(default=False)
    description = serializers.CharField(required=True)
    createdate = serializers.DateField(required=True)
    createtime = serializers.TimeField(required=True)
    createdby = serializers.PrimaryKeyRelatedField(queryset=fyppanel.objects.all())

    class Meta:
        model = notification
        # fields = "__all__"
        fields = ['title', 'description', 'createdate', 'createtime', 'createdby']    
