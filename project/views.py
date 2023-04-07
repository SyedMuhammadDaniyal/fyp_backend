from rest_framework.views import APIView 
from project.serializers import projectSerializer, projectlistSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from core.models import project
from rest_framework.decorators import api_view 


# # Create your views here.
class projectAPIView(APIView):
  def post(self, request):
    serialize = projectSerializer(data=request.data)
    # data1 = project.objects.all()
    # print(data1.id)
    if serialize.is_valid():
      serialize.save()
      return Response(
        {
          "data": serialize.data,
          "message": "success",
          "status": 200
        }
      )
    
    else:
      return Response(
        {
          "data": serialize.errors,
          "message": "already registed",
          "status": 422
        }
      )

@api_view(['GET'])
def projectlist(request):
    sup = project.objects.all()
    serializer = projectlistSerializer(sup, many=True)   
    return Response(serializer.data)
