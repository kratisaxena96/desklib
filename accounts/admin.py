from django.contrib import admin
from accounts.models import UserAccount

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

admin.site.register(UserAccount, UserAdmin)