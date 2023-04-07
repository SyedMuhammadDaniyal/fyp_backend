from rest_framework import generics
from rest_framework.views import APIView 
from milestone.serializers import milestoneSerializer
from core.models import milestone
from rest_framework import viewsets
from rest_framework.response import Response

# # Create your views here.
class milestoneAPIView(APIView):
  def post(self, request):
    serialize = milestoneSerializer(data=request.data)
    
    if serialize.is_valid():
      serialize.save()
      return Response(
        {
          "data": serialize.data,
          "message": "success",
          "status": 200
        }
      )
    
    return Response(
      {
        "data": serialize.errors,
        "message": None,
        "status": 422
      }
    )
