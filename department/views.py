from rest_framework.response import Response
from core.models import department
from .serializers import departmentSerializer
from rest_framework.views import APIView
from django.utils import timezone
from fyp_management.permission import IsFYPPanel
# Create your views here.

class departmentAPI(APIView):
    permission_classes = [IsFYPPanel]

    def get(self, request):
        try:
            sup = department.objects.filter(deleted_at=None)
            serialize = departmentSerializer(sup, many=True)   
            return Response(
                {
                "data":serialize.data,
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

    def post(self, request):
        try:
            serialize = departmentSerializer(data=request.data)
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
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

    def patch(self, request):
        try:
            sup = department.objects.get(id=request.data.get("id"), deleted_at=None)
            serialize = departmentSerializer(sup,data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(
                {
                "data":serialize.data,
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

    def delete(self, request):
        try:
            pk = request.data.get("id")
            my_object = department.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except department.DoesNotExist:
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