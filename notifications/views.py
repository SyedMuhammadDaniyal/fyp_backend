from rest_framework import generics
from rest_framework.views import APIView 
from notifications.serializers import notificationSerializer
from core.models import notification
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# # Create your views here.
class notificationsAPIView(APIView):
  methods = ('POST', 'GET', 'PUT', 'PATCH', 'DELETE')
  def post(self, request):
    serialize = notificationSerializer(data=request.data)
    
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

  def get(self, request):
      my_objects = notification.objects.all()
      serializer = notificationSerializer(my_objects, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
  
  def delete(self, request, pk):
        try:
            my_object = notification.objects.get(pk=pk)
        except notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        my_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

  def put(self, request, pk):
        try:
            my_object = notification.objects.get(pk=pk)
        except notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = notificationSerializer(my_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk):
      try:
          my_object = notification.objects.get(pk=pk)
      except notification.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)

      serializer = notificationSerializer(my_object, data=request.data, partial=True)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)