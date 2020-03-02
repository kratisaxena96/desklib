from django.contrib import admin
from . models import Question, Order, Comment


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']
    raw_id_fields = ['author', 'order']
    list_display = ['message', 'author', 'created']


# Register your models here.
admin.site.register(Question)
admin.site.register(Order)
admin.site.register(Comment, CommentAdmin)
