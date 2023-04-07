from core.models import notification
# from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class notificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    isactive = serializers.BooleanField(default=False)
    description = serializers.CharField(required=True)
    createdate = serializers.DateField(required=True)
    createtime = serializers.TimeField(required=True)
    
    class Meta:
        model = notification
        fields = "__all__"
        # fields = ['milestone_name', 'document_submissin_date', 'milestone_defending_date', 'milestone_details', 'fyp_panel']    
