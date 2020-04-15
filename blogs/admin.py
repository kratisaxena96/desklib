from django.contrib import admin
from blogs.models import BlogModel, BlogCategoryModel

# Register your models here.

class BlogModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'is_visible',  'is_published', 'is_featured','published_date', 'created')
    filter_horizontal = ['category']
    list_filter = ('is_featured',)


admin.site.register(BlogModel, BlogModelAdmin)
admin.site.register(BlogCategoryModel)
