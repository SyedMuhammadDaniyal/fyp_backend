from rest_framework import generics
from rest_framework.views import APIView 
from notifications.serializers import notificationSerializer
from core.models import notification, project
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# # Create your views here.
# class notificationsAPIView(APIView):
#   methods = ('POST', 'GET', 'PUT', 'PATCH', 'DELETE')
#   def post(self, request):
#     serialize = notificationSerializer(data=request.data)
    
#     if serialize.is_valid():
#       serialize.save()
#       return Response(
#         {
#           "data": serialize.data,
#           "message": "success",
#           "status": 200
#         }
#       )
    
#     return Response(
#       {
#         "data": serialize.errors,
#         "message": None,
#         "status": 422
#       }
#     )

#   def get(self, request):
#       my_objects = notification.objects.all()
#       serializer = notificationSerializer(my_objects, many=True)
#       return Response(serializer.data, status=status.HTTP_200_OK)
  
#   def delete(self, request, pk):
#         try:
#             my_object = notification.objects.get(pk=pk)
#         except notification.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         my_object.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#   def put(self, request, pk):
#         try:
#             my_object = notification.objects.get(pk=pk)
#         except notification.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = notificationSerializer(my_object, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#   def patch(self, request, pk):
#       try:
#           my_object = notification.objects.get(pk=pk)
#       except notification.DoesNotExist:
#           return Response(status=status.HTTP_404_NOT_FOUND)

#       serializer = notificationSerializer(my_object, data=request.data, partial=True)
#       if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data, status=status.HTTP_200_OK)
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class createnotificationAPI(APIView):
  def post(self, request):
    try:
        serialize = notificationSerializer(data=request.data)
        if request.data.get('id') != None:                
            if serialize.is_valid():
                notification_obj = serialize.save()
                projects = project.objects.get(id=request.data.get('id')) #get by id (filter)
                # for p in projects:
                print(projects)
                projects.notification.add(notification_obj)
                # projects.save()
                return Response(
                {
                "status": 200,
                "message": "Success",
                "body": {},
                "exception": None
                }
            )            
        elif serialize.is_valid():
            notification_obj = serialize.save()
            projects = project.objects.all()
            for p in projects:
                p.notification.add(notification_obj)
            return Response(
            {
            "status": 200,
            "message": "Success",
            "body": {},
            "exception": None
            }
        )
        else:
            return Response(
            {
                "status": 422,
                "message": serialize.errors,
                "body": {},
                "exception": "some exception"
            }
        )
    except Exception as e:
          return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )


class createnotificationforspecificAPI(APIView):
  def post(self, request):
    try:
        serialize = notificationSerializer(data=request.data)
        if serialize.is_valid():
            notification_obj = serialize.save()
            projects = project.objects.filer(id=request.data.get('id')) #get by id (filter)
            # for p in projects:
            projects.milestone.add(milestone_obj)
            return Response(
            {
            "status": 200,
            "message": "Success",
            "body": {},
            "exception": None
            }
        )
        else:
            return Response(
            {
                "status": 422,
                "message": serialize.errors,
                "body": {},
                "exception": "some exception"
            }
        )
    except Exception as e:
          return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )
