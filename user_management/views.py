from rest_framework.response import Response
from rest_framework.views import APIView
from supervisor.serializers import AddSupervisorSerializer, updateSupervisorSerializer
from teamMember.serializers import teamMemberSerializer, updateStudentSerializer
from core.models import User, teamMember, supervisor
from django.utils import timezone
from rest_framework import status

# Create your views here.
class CreateUserView(APIView):
    def post(self, request):
        try:
            if request.data.get("role") == User.SUPERVISOR:
                serialize = AddSupervisorSerializer(data=request.data)
                if serialize.is_valid():
                    # print(request.data)
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
                        "body": {},
                        "exception": "some exception" 
                        }
                    )
            elif request.data.get("role") == User.STUDENT:            
                serialize = teamMemberSerializer(data=request.data)                        
                if serialize.is_valid():
                    # print(request.data)
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
                        "body": {},
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
            

class allusersAPI(APIView):

    def get(self, request):
        try:
            if request.GET.get("role") == "supervisor":                    
                my_objects = supervisor.objects.filter(deleted_at=None)
                serialize = AddSupervisorSerializer(my_objects, many=True)
                return Response(       
                        {
                        "data": serialize.data,
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )
            elif request.GET.get("role") == "student":
                my_objects = teamMember.objects.filter(deleted_at=None)
                serialize = teamMemberSerializer(my_objects, many=True)
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
                "status": 400,
                "message": "Bad Request",
                "body": {},
                "exception": str(e)
                }
            )


class updatesupervisorAPI(APIView):
    def patch(self, request):
      try:
        sup = supervisor.objects.get(id=request.data.get("id"), deleted_at=None)
        serialize = updateSupervisorSerializer(sup,data=request.data)
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
                "message": "Some e",#serialize.errors
                "body": {},
                "exception": str(e) 
                }
                )


class deletesupervisorAPI(APIView):
      def delete(self, request, pk):
        try:
            my_object = supervisor.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except supervisor.DoesNotExist:
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


class updatestudentAPI(APIView):
    def patch(self, request):
      try:
        sup = teamMember.objects.get(id=request.data.get("id"), deleted_at=None)
        serialize = updateStudentSerializer(sup,data=request.data)
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

class deletestudentAPI(APIView):

      def delete(self, request, pk):
        try:
            my_object = teamMember.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except teamMember.DoesNotExist:
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


class studentlistAPI(APIView):
    def get(self, request):
        sup = teamMember.objects.filter(deleted_at=None)
        serialize = updateStudentSerializer(sup, many=True)   
        return Response(
                        {
                        "data":serialize.data,
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )
