from django.contrib import admin
from blogs.models import BlogModel, BlogCategoryModel

# Register your models here.


admin.site.register(BlogModel)
admin.site.register(BlogCategoryModel)
