from django.urls import path
from .views import RegisterUserAPIView, LoginUserApi, getfyppanel
from project.views import projectAPIView, projectlist
from milestone.views import milestoneAPIView
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
  path('project',projectAPIView.as_view()),
  path('milestone',milestoneAPIView.as_view()),
  path('departmentlist',departmentAPI.as_view()),
  path('getfyppanel',getfyppanel),
  path('projectlist',projectlist),
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

]
