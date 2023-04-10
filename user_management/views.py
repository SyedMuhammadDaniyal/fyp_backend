from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User

# Create your views here.
class CreateUserView(APIView):
    class post(self, request):
        try:
            if request.data.get("role") == User.SUPERVISOR:
                pass
            elif request.data.get("role") == User.STUDENT:
                pass

        except Exception as e:
            return Response(
                {
                "status": 400,
                "message": "Bad Request",
                "body": {},
                "exception": str(e)
                }
            )
