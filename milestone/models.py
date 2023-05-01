from django.db import models

from utils.models import BaseModel

# Create your models here.

class MilestoneWork(BaseModel):
    milestone = models.OneToOneField("core.milestone", on_delete=models.RESTRICT, related_name="milestone_work")
    title = models.CharField(max_length=50)
    description = models.TextField()
    document = models.CharField(max_length=255)
