from django.db import models

from utils.models import BaseModel

# Create your models here.
# class Sprint(BaseModel):
#     project = models.ForeignKey("core.project", on_delete=models.RESTRICT)
#     milestone = models.ForeignKey("core.milestone", on_delete=models.RESTRICT)
#     title = models.CharField(max_length=125)
#     start_date = models.DateField()
#     end_date = models.DateField()

# class Ticket(BaseModel):
#     sprint = models.ForeignKey("boards.Sprint", on_delete=models.RESTRICT)
#     title = models.CharField(max_length=125)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     assignee = models.ForeignKey("core.User", on_delete=models.RESTRICT)
