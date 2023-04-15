from django.urls import path
from .views import RegisterUserAPIView, LoginUserApi, getfyppanel
from project.views import projectAPIView, projectlistAPI, updateprojectAPI, deleteprojectAPI, addteammemberAPI
from milestone.views import createmilestoneAPI, allmilestoneAPI, updatemilestoneAPI, deletemilestoneAPI, GetAllMilestones
from supervisor.views import supervisorView
from department.views import departmentAPI
from notifications.views import notificationsAPIView
from teamMember.views import RegisterteamMemberAPIView
from user_management.views import CreateUserView, allusersAPI, updatesupervisorAPI, studentlistAPI, deletesupervisorAPI, updatestudentAPI, deletestudentAPI
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
  path('register',RegisterUserAPIView.as_view()),
  path('login', LoginUserApi.as_view()),
  path('departmentlist',departmentAPI.as_view()),
  path('getfyppanel',getfyppanel),
  path('createnotification',notificationsAPIView.as_view(methods=['post','get'])),
  path('deletenotification/<int:pk>/', notificationsAPIView.as_view(methods=['delete']), name='myapi-delete'),
  path('updatenotification/<int:pk>/', notificationsAPIView.as_view(methods=['put', 'patch']), name='myapi-update'),
  path('teamMemberRegister',RegisterteamMemberAPIView.as_view()),
  path('createUser', CreateUserView.as_view()),
  path('alluser/', allusersAPI.as_view()),
  path('updatesupervisor', updatesupervisorAPI.as_view()),
  path('deletesupervisor/<int:pk>', deletesupervisorAPI.as_view()),
  path('studentlist',studentlistAPI.as_view()),
  path('updatestudent', updatestudentAPI.as_view()),
  path('deletestudent/<int:pk>', deletestudentAPI.as_view()),
  path('createproject',projectAPIView.as_view()),
  path('updateproject',updateprojectAPI.as_view()),
  path('projectlist',projectlistAPI.as_view()),
  path('deleteproject/<int:pk>',deleteprojectAPI.as_view()),
  path('addteammember',addteammemberAPI.as_view()),
  path('createmilestone',createmilestoneAPI.as_view()),
  path('allmilestone', allmilestoneAPI.as_view()),
  path('updatemilestone',updatemilestoneAPI.as_view()),
  path('deletemilestone/<int:pk>', deletemilestoneAPI.as_view()),
  path('getallmilestone', GetAllMilestones.as_view()),
]
