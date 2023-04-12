from django.shortcuts import render
from rest_framework.response import Response
from core.models import department
# from rest_framework.decorators import api_view 
from .serializers import departmentSerializer
from rest_framework.views import APIView
# Create your views here.

class departmentAPI(APIView): 
    def get(self, request):
        sup = department.objects.all()
        serializer = departmentSerializer(sup, many=True)   
        return Response(serializer.data)
