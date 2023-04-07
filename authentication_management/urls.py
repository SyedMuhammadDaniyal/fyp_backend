from django.urls import path
from .views import RegisterUserAPIView, LoginUserApi, getfyppanel
from project.views import projectAPIView, projectlist
from milestone.views import milestoneAPIView
from supervisor.views import supervisorView
from department.views import departmentView
from notifications.views import notificationsAPIView
from teamMember.views import RegisterteamMemberAPIView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
  path('register',RegisterUserAPIView.as_view()),
  path('login', LoginUserApi.as_view()),
  path('project',projectAPIView.as_view()),
  path('milestone',milestoneAPIView.as_view()),
  path('supervisorlist',supervisorView),
  path('departmentlist',departmentView),
  path('getfyppanel',getfyppanel),
  path('projectlist',projectlist),
  path('createnotification',notificationsAPIView.as_view(methods=['post','get'])),
  path('deletenotification/<int:pk>/', notificationsAPIView.as_view(methods=['delete']), name='myapi-delete'),
  path('updatenotification/<int:pk>/', notificationsAPIView.as_view(methods=['put', 'patch']), name='myapi-update'),
  path('teamMemberRegister',RegisterteamMemberAPIView.as_view())
]
