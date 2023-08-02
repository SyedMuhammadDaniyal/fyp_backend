from django.contrib import admin
from core.models import supervisor, department, project, milestone, fyppanel, User, notification, teamMember, University
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    # ... other admin configuration ...

    def delete_view(self, request, object_id, extra_context=None):
        # Get the user being deleted
        user = User.objects.get(pk=object_id)

        # Check if the user is a superuser
        if user.is_superuser and user == request.user:
            self.message_user(request, "You cannot delete yourself as a superuser.")
            return self.response_post_save_change(request, None)

        return super().delete_view(request, object_id, extra_context)

# Register your models here.
admin.site.register(supervisor)
admin.site.register(department)
admin.site.register(project)
admin.site.register(milestone)
admin.site.register(fyppanel)
admin.site.register(User, CustomUserAdmin)
admin.site.register(notification)
admin.site.register(teamMember)
admin.site.register(University)
