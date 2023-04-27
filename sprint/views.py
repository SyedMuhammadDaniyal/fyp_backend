from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import sprintSerializer
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
