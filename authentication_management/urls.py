from django.urls import path
from .views import RegisterUserAPIView, LoginUserApi, getfyppanel
from project.views import projectAPIView, projectlistAPI, updateprojectAPI, deleteprojectAPI, addteammemberAPI, allprojectAPI
from milestone.views import createmilestoneAPI, allmilestoneAPI, updatemilestoneAPI, deletemilestoneAPI, GetAllMilestones
from supervisor.views import supervisorView
from department.views import departmentAPI
from notifications.views import createnotificationAPI, allnotificationsAPI, getallnotificationsAPI, deletenotificationAPI, updatenotificationAPI
from teamMember.views import RegisterteamMemberAPIView
from user_management.views import CreateUserView, allusersAPI, updatesupervisorAPI, studentlistAPI, deletesupervisorAPI, updatestudentAPI, deletestudentAPI
from sprint.views import createsprintAPI
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
  path('registerpmo',RegisterUserAPIView.as_view()),
  path('login', LoginUserApi.as_view()),
  path('departmentcrud',departmentAPI.as_view()),
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
  path('projects',allprojectAPI.as_view()), 
  path('deleteproject/<int:pk>',deleteprojectAPI.as_view()),
  path('addteammember',addteammemberAPI.as_view()),
  path('createmilestone',createmilestoneAPI.as_view()),
  path('allmilestone', allmilestoneAPI.as_view()),
  path('updatemilestone',updatemilestoneAPI.as_view()),
  path('deletemilestone/<int:pk>', deletemilestoneAPI.as_view()),
  path('getallmilestone', GetAllMilestones.as_view()),
  path('createnotification',createnotificationAPI.as_view()),
  path('allnotifications', allnotificationsAPI.as_view()),
  path('getallnotifications', getallnotificationsAPI.as_view()),
  path('deletenotification/<int:pk>', deletenotificationAPI.as_view()),
  path('updatenotification', updatenotificationAPI.as_view()),
  path('createsprint', createsprintAPI.as_view()),
]
