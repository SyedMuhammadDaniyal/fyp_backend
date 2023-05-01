from django.urls import path

from milestone import views


urlpatterns = [
    path("work", views.MilestoneSubmissionView.as_view(), name="submit_milestone_work")
]