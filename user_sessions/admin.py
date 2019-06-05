from django.contrib import admin
from user_sessions.models import UserSession


class UserSessionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserSession, UserSessionAdmin)

