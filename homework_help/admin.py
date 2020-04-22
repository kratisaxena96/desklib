from django.contrib import admin
from . models import Question, Order, Comment, Answers, QuestionFile, AnswerFile


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']
    raw_id_fields = ['author', 'order']
    list_display = ['message', 'order', 'author', 'created']



class QuestionFileAdmin(admin.TabularInline):
    # form = SampleFileAdminForm
    model = QuestionFile
    extra = 1

    # readonly_fields = ('author',)
    raw_id_fields = ('author',)


class AnswerFileAdmin(admin.TabularInline):
    # form = SampleFileAdminForm
    model = AnswerFile
    extra = 1

    # readonly_fields = ('author',)
    raw_id_fields = ('author',)


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionFileAdmin, ]
    readonly_fields = ['created', 'updated', 'uid']
    prepopulated_fields = {'slug': ('question', )}
    list_display = ['question', 'subjects', 'is_visible', 'is_published', 'created']
    list_filter = ('is_visible',  'is_published', 'subjects',)
    search_fields = ['question',]
    raw_id_fields = ['subjects', 'author']


class AnswerAdmin(admin.ModelAdmin):
    inlines = [AnswerFileAdmin, ]
    readonly_fields = ['created', 'updated', 'answer_id']
    list_display = ['question', 'is_visible', 'is_published', 'created']
    list_filter = ('is_visible',  'is_published',)
    search_fields = ['question__question',]
    raw_id_fields = ['question', 'author']


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'uuid']


class QuestionFileAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'unique_id']
    raw_id_fields = ['question', 'author']


class AnswerFileAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'unique_id']
    raw_id_fields = ['answer', 'author']

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionFile, QuestionFileAdmin)
admin.site.register(AnswerFile, AnswerFileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Answers, AnswerAdmin)

