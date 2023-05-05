from core.models import milestone, fyppanel
from .models import MilestoneWork
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class milestoneSerializer(serializers.ModelSerializer):
    milestone_name = serializers.CharField(required=True)
    document_submission_date = serializers.DateField(required=True)
    milestone_defending_date = serializers.DateField(required=True)
    milestone_details = serializers.CharField(required=True)
    rubrics = serializers.JSONField(required=True)
    marks = serializers.FloatField(required=True)
    class Meta:
        model = milestone
        fields = ['id','milestone_name', 'document_submission_date', 'milestone_defending_date', 'milestone_details', 'rubrics', 'marks']


class milestoneworkSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    document = serializers.CharField(required=True)

    class Meta:
        model = MilestoneWork
        fields = "__all__"