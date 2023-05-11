import base64
from fyp_management.permission import IsFYPPanel, IsStudent, IsSupervisor
from rest_framework.views import APIView
from milestone.serializers import milestoneSerializer, milestoneworkSerializer, milestonemarkSerializer
from core.models import milestone, project, supervisor
from rest_framework.response import Response
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from datetime import datetime
from fyp_management.settings import imagekit
from milestone.models import MilestoneWork
from core.models import milestone
from core.models import milestone, project, supervisor, teamMember, User
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from .models import Milestonemarks
# # Create your views here.
class createmilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def post(self, request):
        try:
            serialize = milestoneSerializer(data=request.data)
            if serialize.is_valid():
                milestone_obj = serialize.save()
                projects = project.objects.filter(status="ongoing", deleted_at=None)
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
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def get(self, request):
        try:
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
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class updatemilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
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
                "message": "Some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class deletemilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
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
        return Response({
            "status": 200,
            "message": "Successfuly deleted",
            "body": {},
            "exception": None 
            }
        )


class GetAllMilestones(APIView):
    permission_classes = [IsAuthenticated & (IsSupervisor | IsStudent)]

    def get(self, request):
        try:
            if request.user.role == User.SUPERVISOR:
                sup = supervisor.objects.get(user=request.user, deleted_at=None)
                projects = project.objects.filter(supervisor=sup)
                if len(projects) != 0:
                    milestones = milestone.objects.filter(project=projects[0], deleted_at=None)
                    serializer = milestoneSerializer(milestones, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                        }
                    )
                else:
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": [],
                        "exception": None
                        }
                    )
            elif request.user.role == User.STUDENT:
                tm = teamMember.objects.get(user=request.user, deleted_at=None)
                pro = tm.project
                if pro != None:
                    milestones = milestone.objects.filter(project=pro, deleted_at=None)
                    serializer = milestoneSerializer(milestones, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                        }
                    )
                else:
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": [],
                        "exception": None
                        }
                    )
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
                }
            )
        

class SubmissionView(APIView):
    permission_classes = [IsAuthenticated & (IsFYPPanel | IsSupervisor | IsStudent)]

    def get(self, request):
        try:
            mil = milestone.objects.filter(project=project.objects.get(id=request.data.get("project_id"), deleted_at=None))
            milestone_work = MilestoneWork.objects.filter(milestone__in=mil, deleted_at=None)
            serialize = milestoneworkSerializer(milestone_work, many=True)
            data = serialize.data
            response = {}
            for m in mil:
                milestone_work_data = [d for d in data if d["milestone"] == m.id]
                response[m.milestone_name] = milestone_work_data
            return Response({
                "status": 200,
                "message": "Success",
                "body": response,
                "exception": None
                }
            )
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
                }
            )

class MilestoneSubmissionView(APIView):
    permission_classes = [IsAuthenticated & IsStudent]

    def post(self, request):
        try:
            m = milestone.objects.get(id=request.data.get('milestone_id'), deleted_at=None)
            t = m.milestone_name
            options = UploadFileRequestOptions(
                use_unique_file_name=False,
                tags=['abc', 'def'],
                folder=f"/milestone/work/{t}/",
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
                milestone_work = MilestoneWork.objects.get(project=request.data.get("project_id"), milestone=request.data.get("milestone_id"), deleted_at=None)
                milestone_work.title=request.data.get("title")
                milestone_work.description=request.data.get("description")
                milestone_work.project=project.objects.get(id=request.data.get("project_id"))
                milestone_work.milestone=milestone.objects.get(id=request.data.get("milestone_id"))
                milestone_work.document=upload_response.url
                milestone_work.save()
                return Response({
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )
            except:
                MilestoneWork.objects.create(
                    milestone=milestone.objects.get(id=request.data.get("milestone_id")),
                    title=request.data.get("title"),
                    description=request.data.get("description"),
                    project=project.objects.get(id=request.data.get("project_id")),
                    document=upload_response.url
                )
                return Response({
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
                }
            )


class givemarksView(APIView):
    permission_classes = [IsAuthenticated & (IsFYPPanel | IsSupervisor)]
    
    def post(self, request):
        try:
            mk = Milestonemarks.objects.filter(project=request.data.get("project"),milestone=request.data.get("milestone"), m_distributor=request.data.get("m_distributor"), deleted_at=None)
            if len(mk) > 0:
                return Response(
                    {
                    "status": 200,
                    "message": "This form is allowed once submission",
                    "body": {},
                    "exception": None
                    }
                )
            else:
                serialize = milestonemarkSerializer(data=request.data)
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

class marksView(APIView):
    permission_classes = [IsAuthenticated & (IsFYPPanel | IsSupervisor | IsStudent)]

    def get(self, request):
        try:
            mk = Milestonemarks.objects.filter(project = project.objects.get(id=request.data.get("project"), deleted_at=None, status="ongoing"), deleted_at=None)
            mil = milestone.objects.get(id = request.data.get("milestone"), deleted_at=None)
            current_date = datetime.now().date()
            milestone_date = mil.milestone_defending_date
            date_difference = current_date - milestone_date
            if date_difference.days == 0 or date_difference.days < 0:
                return Response(
                    {
                    "status": 200,
                    "message": "Marks are updated after "+str(milestone_date)+" date",
                    "body": {},
                    "exception": None
                    }
                )
            else:
                mark = []
                for m in mk:
                    mark.append(m.marks)
                if len(mark) == 0:
                    return Response(       
                        {
                        "status": 400,
                        "message": "Doest not have Marks Rightnow",
                        "body": {},
                        "exception": "zero division" 
                        }
                    )
                else:
                    average = sum(mark)/len(mark)
                    return Response(
                        {
                        "status": 200,
                        "message": "Success",
                        "Milestone Marks": average,
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
