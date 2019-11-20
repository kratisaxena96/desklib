from django.contrib import admin
from .models import Review
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('title', 'email', 'stars', 'description', 'is_published', 'name',)
    list_filter = ('is_published',)


admin.site.register(Review, ReviewAdmin)
