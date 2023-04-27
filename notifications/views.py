from rest_framework import generics
from rest_framework.views import APIView 
from notifications.serializers import notificationSerializer
from core.models import notification, project, supervisor
from rest_framework.response import Response
from django.utils import timezone
# # Create your views here.

class createnotificationAPI(APIView):
  def post(self, request):
    try:
        serialize = notificationSerializer(data=request.data)
        if request.data.get('id') != None:                
            if serialize.is_valid():
                notification_obj = serialize.save()
                projects = project.objects.get(id=request.data.get('id')) #get by id (filter)
                print(projects)
                projects.notification.add(notification_obj)
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

class allnotificationsAPI(APIView):
    #for pmo
    def get(self, request):
        try:
            my_objects = notification.objects.filter(deleted_at=None)
            serializer = notificationSerializer(my_objects, many=True)
            return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                    })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })


class getallnotificationsAPI(APIView):
    def get(self, request):
        try:
            if request.data.get("role") == "supervisor": #hardcode
                sup = supervisor.objects.get(id=request.data.get("supervisorid"), deleted_at=None)
                projects = project.objects.filter(supervisor=sup)
                if projects != None:
                    notifications = notification.objects.filter(project=projects[0], deleted_at=None)
                    serializer = notificationSerializer(notifications, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                    })
            elif request.data.get("role") == "student": #hardcode
                p = project.objects.get(id=request.data.get("projectid"), deleted_at=None)
                if p != None:
                    notifications = notification.objects.filter(project=p, deleted_at=None)
                    serializer = notificationSerializer(notifications, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                    })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })

class deletenotificationAPI(APIView):    
    def delete(self, request, pk):
        try:
            my_object = notification.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except notification.DoesNotExist:
            return Response(
                        {
                        "status": 404,
                        "message": "Not Found",
                        "body": {},
                        "exception": None 
                        }
                    )
        return Response(
                        {
                        "status": 200,
                        "message": "Successfuly deleted",
                        "body": {},
                        "exception": None 
                        }
                    )

class updatenotificationAPI(APIView):
    def patch(self, request):
        try:
            sup = notification.objects.get(id=request.data.get("id"), deleted_at=None)
            serialize = notificationSerializer(sup,data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(       
                        {
                        "data": serialize.data,
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
                    "message": serialize.errors,
                    "body": {},
                    "exception": str(e) 
                    }
                )
