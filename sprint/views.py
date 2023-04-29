from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import sprintSerializer
from .models import Sprint
from django.utils import timezone
from core.models import project, User, supervisor
# Create your views here.

class createsprintAPI(APIView):
  def post(self, request):
    try:
        serialize = sprintSerializer(data=request.data)
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

class getspecificsprintAPI(APIView):
        permission_classes = [IsAuthenticated]
        def get(self, request):
            try:
                if request.user.role == User.SUPERVISOR:
                    sup = supervisor.objects.get(user=request.user)
                    # pro = list(project.objects.filter(supervisor=request.data.get("id"), deleted_at=None)).values_list('id', flat=True)
                    # pk = pro.pop()
                    sp = Sprint.objects.filter(project__in=sup.projects, deleted_at=None)
                    serialize = sprintSerializer(sp, many=True)
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
                    "message": serialize.errors,
                    "body": {},
                    "exception": str(e) 
                    }
                )


class updatesprintAPI(APIView):
    def patch(self, request):
        try:
            sp = Sprint.objects.get(id=request.data.get("id"), deleted_at=None)
            serialize = sprintSerializer(sp,data=request.data)
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

class deletesprintAPI(APIView):

    def delete(self, request, pk):
        try:
            my_object = Sprint.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except Sprint.DoesNotExist:
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