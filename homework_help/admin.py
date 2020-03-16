from django.contrib import admin
from . models import Question, Order, Comment, Answers, QuestionFile


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']
    raw_id_fields = ['author', 'order']
    list_display = ['message', 'order', 'author', 'created']



class QuestionFileAdmin(admin.TabularInline):
    # form = SampleFileAdminForm
    model = QuestionFile
    extra = 1
    min_num = 2

    # readonly_fields = ('author',)
    raw_id_fields = ('author',)


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionFileAdmin, ]


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']


class QuestionFileAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'unique_id']
    raw_id_fields = ['question', 'author']

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionFile, QuestionFileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Answers)

