from django.contrib import admin
from .models import Review
# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('stars', 'review', 'is_published', 'author',)
    list_filter = ('is_published',)


admin.site.register(Review, ReviewAdmin)
