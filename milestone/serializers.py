from core.models import milestone, fyppanel
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class milestoneSerializer(serializers.ModelSerializer):
    milestone_name = serializers.CharField(required=True)
    document_submissin_date = serializers.DateField(required=True)
    milestone_defending_date = serializers.DateField(required=True)
    milestone_details = serializers.CharField(required=True)
    rubrics = serializers.JSONField()
    fyp_panel = serializers.PrimaryKeyRelatedField(queryset=fyppanel.objects.all())

    class Meta:
        model = milestone
        # fields = "__all__"
        fields = ['id','milestone_name', 'document_submissin_date', 'milestone_defending_date', 'milestone_details', 'rubrics', 'fyp_panel']    
