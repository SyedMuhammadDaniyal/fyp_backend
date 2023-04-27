from rest_framework.views import APIView 
from django.shortcuts import get_object_or_404
from project.serializers import projectSerializer, projectlistSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from core.models import project, teamMember
from rest_framework.decorators import api_view 
from django.utils import timezone
from teamMember.serializers import teamMemberSerializer
# from rest_framework.permissions import IsAuthenticated

# # Create your views here.
class projectAPIView(APIView):
    # permission_classes = [IsAuthenticated]
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
    def get(self, request):
        try:
            if request.data.get("role") == "supervisor": #hardcode
                sup = project.objects.filter(supervisor=request.data.get("id"), deleted_at=None)
                serialize = projectlistSerializer(sup, many=True)   
                return Response(       
                            {
                            "data": serialize.data,
                            "status": 200,
                            "message": "Success",
                            "body": {},
                            "exception": None 
                            }
                        )
            elif request.data.get("role") == "student": #hardcode
                tm = teamMember.objects.get(id=request.data.get("id"), deleted_at=None)
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
                    "message": serialize.errors,
                    "body": {},
                    "exception": str(e) 
                    }
                )

class deleteprojectAPI(APIView):
    
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
        tm.project = None
        tm.save()
        return Response(
                        {
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )
    
class allprojectAPI(APIView):
    def get(self, request):
        try:
            my_objects = project.objects.filter(deleted_at=None)
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
