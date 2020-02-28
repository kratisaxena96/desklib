from django.contrib import admin
from . models import Question, Order, Comment, Answers


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']

# Register your models here.
admin.site.register(Question)
admin.site.register(Order)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Answers)

