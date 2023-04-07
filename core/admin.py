from django.contrib import admin
from core.models import supervisor, department, project, milestone, fyppanel, User, notification, teamMember


# Register your models here.
admin.site.register(supervisor)
admin.site.register(department)
admin.site.register(project)
admin.site.register(milestone)
admin.site.register(fyppanel)
admin.site.register(User)
admin.site.register(notification)
admin.site.register(teamMember)
