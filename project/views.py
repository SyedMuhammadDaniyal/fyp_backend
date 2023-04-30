from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, fyppanel, project, supervisor, teamMember
from project.serializers import projectlistSerializer, projectSerializer

# from rest_framework.permissions import IsAuthenticated

# # Create your views here.
class projectAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serialize = projectSerializer(data=request.data)
            if serialize.is_valid():
                serialize.save()
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
                    "body":{},
                    "exception": "some exception"
                    }
                )
        except Exception as e:
            return Response(
                {
            "status": 400,
            "message": "Bad Request",
            "body": {},
            "exception": str(e)
            }
        )


class projectlistAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            if request.user.role == User.SUPERVISOR:
                sup = supervisor.objects.get(user=request.user, deleted_at=None)
                pro = project.objects.filter(supervisor=sup, deleted_at=None)
                serialize = projectlistSerializer(pro, many=True)   
                return Response(       
                            {
                            "data": serialize.data,
                            "status": 200,
                            "message": "Success",
                            "body": {},
                            "exception": None 
                            }
                        )
            elif request.user.role == User.STUDENT:
                tm = teamMember.objects.get(user=request.user, deleted_at=None)
                pro = tm.project
                serialize = projectlistSerializer(pro)   
                return Response(       
                            {
                            "data": serialize.data,
                            "status": 200,
                            "message": "Success",
                            "body": {},
                            "exception": None 
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
        

class updateprojectAPI(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            sup = project.objects.get(id=request.data.get("id"), deleted_at=None)
            serialize = projectSerializer(sup,data=request.data)
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
                    "message": "some exception",
                    "body": {},
                    "exception": str(e) 
                    }
                )

class deleteprojectAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            my_object = project.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except project.DoesNotExist:
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

class addteammemberAPI(APIView):
    permission_classes = [IsAuthenticated]    
    def post(self, request):
        pro = project.objects.get(id=request.data.get("project_id"), deleted_at=None)
        tm = teamMember.objects.get(id=request.data.get("teammember_id"), deleted_at=None)
        tm.project = pro
        tm.save()
        return Response(
                        {
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )

    def delete(self, request):
        pro = project.objects.get(id=request.data.get("project_id"), deleted_at=None)
        tm = teamMember.objects.get(id=request.data.get("teammember_id"), deleted_at=None)
        if tm.project == None:
                return Response(
                        {
                        "status": 404,
                        "message": "Not Found",
                        "body": {},
                        "exception": None 
                        }
                    )
        else:    
            tm.project = None
            tm.save()
            return Response(
                    {
                    "status": 200,
                    "message": "Successfuly deleted",
                    "body": {},
                    "exception": None 
                    }
                )
                    
    
class allprojectAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            pmo = fyppanel.objects.get(user=request.user, deleted_at=None)
            my_objects = project.objects.filter(department=pmo.user.department, deleted_at=None)
            serializer = projectlistSerializer(my_objects, many=True)
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

class changesupervisorAPI(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            pro = project.objects.get(id=request.data.get("pro_id"), deleted_at=None)
            sup = supervisor.objects.get(id=request.data.get("sup_id"), deleted_at=None)
            pro.supervisor = sup
            pro.save()
            return Response(       
                    {
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None 
                    }
                )
               
        except Exception as e:
            return Response(       
                    {
                    "status": 404,
                    "body": {},
                    "exception": str(e) 
                    }
                )

