from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from fyp_management.permission import IsFYPPanel, IsStudent, IsSupervisor
from core.models import User, fyppanel, project, supervisor, teamMember, milestone
from project.serializers import projectlistSerializer, projectSerializer
from teamMember.serializers import teamMemberSerializer
from milestone.models import Milestonemarks
# from rest_framework.permissions import IsAuthenticated

# # Create your views here.
class projectAPIView(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def post(self, request):
        department = request.user.department
        dep_id = department.id
        try:
            # Assuming you have the 'request' object with the JSON data
            # Fetching values from request.data dynamically
            
            json_title = request.data.get("title")
            json_year = request.data.get("year")
            json_batch = request.data.get("batch")
            json_description = request.data.get("description")
            json_domain = request.data.get("domain")
            json_no_of_group_members = int(request.data.get("no_of_group_members"))
            json_supervisor = int(request.data.get("supervisor"))

            # Creating the dictionary
            data = {
                'title': json_title,
                'year': json_year,
                'batch': json_batch,
                'description': json_description,
                'domain': json_domain,
                'no_of_group_members': json_no_of_group_members,
                'supervisor': json_supervisor,
                'department': dep_id
            }
            serialize = projectSerializer(data=data)
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
                    "exception": "Validation Error",
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
    permission_classes = [IsAuthenticated & (IsSupervisor | IsStudent)]
    def get(self, request):
        try:
            if request.user.role == User.SUPERVISOR:
                sup = supervisor.objects.get(user=request.user, deleted_at=None)
                pro_queryset = project.objects.filter(supervisor=sup, deleted_at=None)
                data = []
                for pro in pro_queryset:
                    team_member = teamMember.objects.filter(project_id=pro.id, deleted_at=None)
                    current_no_of_group_members = len(team_member)
                    serialize = projectlistSerializer(pro)
                    project_data = serialize.data 
                    data_dict = {
                        'current_no_of_group_members': current_no_of_group_members,
                        **project_data
                    }
                    data.append(data_dict)
                return Response(       
                            {
                            "data": data,
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
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def patch(self, request):
        try:
            try:
                sup = project.objects.get(id=request.data.get("id"), deleted_at=None)
                team_member = teamMember.objects.filter(project__id=request.data.get("id"), deleted_at=None)
                if len(team_member) > request.data.get("no_of_group_members"):
                    return Response(       
                            {
                            "data": [],
                            "status": 200,
                            "message": "You are not allowed to decrease number of group members becuase there are already more group members than your specified limit, In order to decrease group members. ask supervisor to remove some members from project",
                            "body": {},
                            "exception": None 
                            }
                        )
                else:
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
            except:
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
    permission_classes = [IsAuthenticated & IsFYPPanel]
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
    permission_classes = [IsAuthenticated & IsSupervisor]
    def post(self, request):
        try:
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
        except Exception as e:
            return Response(       
                    {
                    "status": 404,
                    "message": "some exception",
                    "body": {},
                    "exception": str(e) 
                    }
                )
            
    
class allprojectAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def get(self, request):
        try:
            dep_id = request.user.department
            my_objects = project.objects.filter(department=dep_id, deleted_at=None)
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
    permission_classes = [IsAuthenticated & IsFYPPanel]
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

class studentprojectwiseAPI(APIView):
    permission_classes = [IsAuthenticated & (IsSupervisor | IsStudent | IsFYPPanel)]
    def get(self, request):
        try:
            tm = teamMember.objects.filter(project=project.objects.get(id=request.GET.get("pro_id")), deleted_at=None)
            serialize = teamMemberSerializer(tm, many=True)
            return Response({
                "status": 200,
                "message": "Success",
                "body": serialize.data,
                "exception": None
            })
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
            })

class markasCompletedApi(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]

    def patch(self, request):
        try:
            pro=project.objects.get(id=request.data.get("pro_id"), deleted_at=None)            
            if request.data.get("status") == "completed":
                milestone_marks = Milestonemarks.objects.filter(project=pro, deleted_at=None)
                milestone_marks_dict = {}
                for milestone_mark in milestone_marks:
                    if milestone_mark.milestone_id not in milestone_marks_dict:
                        milestone_marks_dict[milestone_mark.milestone_id] = []
                    milestone_marks_dict[milestone_mark.milestone_id].append(milestone_mark.marks)
                averages = {key: sum(values) / len(values) for key, values in milestone_marks_dict.items()}
                grad = 0
                for i in averages:
                    grad += averages[i]
                pro.status = request.data.get("status")
                pro.grade = grad
                pro.save()
                return Response({
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                })
            else:
                pro.status = request.data.get("status")
                pro.grade = 0
                pro.save()
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
