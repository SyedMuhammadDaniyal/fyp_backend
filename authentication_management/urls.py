from django.urls import path
from .views import RegisterUserAPIView, LoginUserApi


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
  path('register',RegisterUserAPIView.as_view()),
  # path('login', LoginUserApi.as_view()),
  path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
