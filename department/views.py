from django.shortcuts import render
from rest_framework.response import Response
from core.models import department
from rest_framework.decorators import api_view 
from .serializers import departmentSerializer

# Create your views here.

@api_view(['GET'])
def departmentView(request):
    sup = department.objects.all()
    serializer = departmentSerializer(sup, many=True)   
    return Response(serializer.data)
