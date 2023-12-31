from django.contrib import admin
from user_sessions.models import UserSession


class UserSessionAdmin(admin.ModelAdmin):
    search_fields = ['user__username',]
    raw_id_fields = ('user','session')
    list_display = ('user','user_agent','created','last_activity')


admin.site.register(UserSession, UserSessionAdmin)

