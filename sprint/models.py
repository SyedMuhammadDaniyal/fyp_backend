from django.db import models
from utils.models import BaseModel

# Create your models here.
class Sprint(BaseModel):
    project = models.ForeignKey("core.project", on_delete=models.RESTRICT)
    milestone = models.ForeignKey("core.milestone", on_delete=models.RESTRICT)
    title = models.CharField(max_length=125)
    start_date = models.DateField()
    end_date = models.DateField()

class Ticket(BaseModel):
    TODO="todo"
    INPROGRESS="inprogress"
    REVIEW="review"
    COMPLETED="completed"

    kanban_status = (
        (TODO, TODO),
        (INPROGRESS, INPROGRESS),
        (REVIEW, REVIEW),
        (COMPLETED, COMPLETED)  
    )
    sprint = models.ForeignKey(Sprint, on_delete=models.RESTRICT)
    title = models.CharField(max_length=125)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(choices=kanban_status, max_length=30, default=TODO)
    creator = models.ForeignKey("core.User", on_delete=models.RESTRICT, related_name='creator')
    assignee = models.ForeignKey("core.User", on_delete=models.RESTRICT, related_name='assignee')