from rest_framework.response import Response
from django.shortcuts import render
from core.models import supervisor, department
from .serializers import supervisorSerializer
from rest_framework.decorators import api_view 
# Create your views here.

# @api_view(['GET'])
# def supervisorView(request):
#     context = supervisor.objects.all()
#     print(context)
#     return context


@api_view(['GET'])
def supervisorView(request):
    sup = supervisor.objects.all()
    serializer = supervisorSerializer(sup, many=True)   
    return Response(serializer.data)
