from core.models import milestone
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class milestoneSerializer(serializers.ModelSerializer):
    milestone_name = serializers.CharField(required=True)
    document_submissin_date = serializers.DateField()
    milestone_defending_date = serializers.DateField()
    milestone_details = serializers.CharField(required=True)
    
    class Meta:
        model = milestone
        fields = "__all__"
        # fields = ['milestone_name', 'document_submissin_date', 'milestone_defending_date', 'milestone_details', 'fyp_panel']    
