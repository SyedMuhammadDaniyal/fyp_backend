import base64

from rest_framework.views import APIView
from milestone.serializers import milestoneSerializer
from core.models import milestone, project, supervisor
from rest_framework.response import Response
from django.utils import timezone
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from fyp_management.settings import imagekit
from milestone.models import MilestoneWork
from core.models import milestone

# # Create your views here.
class createmilestoneAPI(APIView):
  def post(self, request):
    try:
        serialize = milestoneSerializer(data=request.data)
        if serialize.is_valid():
            milestone_obj = serialize.save()
            projects = project.objects.all()
            for p in projects:
                p.milestone.add(milestone_obj)
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

class allmilestoneAPI(APIView):
    def get(self, request):
        mil = milestone.objects.filter(deleted_at=None)
        serialize = milestoneSerializer(mil, many=True) #, many=True   
        return Response(
                    {
                        "data":serialize.data,
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )

class updatemilestoneAPI(APIView):

    def patch(self, request):
      try:
        sup = milestone.objects.get(id=request.data.get("id"), deleted_at=None)
        serialize = milestoneSerializer(sup,data=request.data)
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

class deletemilestoneAPI(APIView):

      def delete(self, request, pk):
        try:
            my_object = milestone.objects.get(pk=pk, deleted_at=None)
            my_object.deleted_at = timezone.now()
            my_object.save()
        except milestone.DoesNotExist:
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


class GetAllMilestones(APIView):
    def get(self, request):
        try:
            if request.data.get("role") == "supervisor": #hardcode
                sup = supervisor.objects.get(id=request.data.get("supervisorid"), deleted_at=None)
                projects = project.objects.filter(supervisor=sup)
                if projects != None:
                    milestones = milestone.objects.filter(project=projects[0], deleted_at=None)
                    serializer = milestoneSerializer(milestones, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                    })
            elif request.data.get("role") == "student": #hardcode
                p = project.objects.get(id=request.data.get("projectid"), deleted_at=None)
                if p != None:
                    milestones = milestone.objects.filter(project=p, deleted_at=None)
                    serializer = milestoneSerializer(milestones, many=True)
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
        

class MilestoneSubmissionView(APIView):
    def get(self, request):
        try:
            milestone_work = MilestoneWork.objects.get(milestone=milestone.objects.get(id=request.GET.get("milestone_id")))
            response = {
                "title": milestone_work.title,
                "description": milestone_work.description,
                "document": milestone_work.document,
                "milestone_id": milestone_work.milestone.id
            }
            return Response({
                "status": 200,
                "message": "Success",
                "body": response,
                "exception": None
            })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })

    def post(self, request):
        try:
            options = UploadFileRequestOptions(
                use_unique_file_name=False,
                tags=['abc', 'def'],
                folder=f"/milestone/work/{request.data.get('milestone_id')}/",
            )
            with request.FILES['file'].open("rb") as file:
                file = base64.b64encode(file.read())
            # Upload the file to ImageKit
            upload_response = imagekit.upload_file(
                file=file,
                file_name=f"{request.FILES['file'].name}",
                options=options
            )

            try:
                milestone_work = MilestoneWork.objects.get(milestone=milestone.objects.get(id=request.data.get("milestone_id")))
                milestone_work.title=request.data.get("title"),
                milestone_work.description=request.data.get("description"),
                milestone_work.document=upload_response.url
                milestone_work.save()
            except:
                MilestoneWork.objects.create(
                    milestone=milestone.objects.get(id=request.data.get("milestone_id")),
                    title=request.data.get("title"),
                    description=request.data.get("description"),
                    document=upload_response.url
                )
            return Response({
                "status": 200,
                "message": "Success",
                "body": {},
                "exception": None
            })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })
