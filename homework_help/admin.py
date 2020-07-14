from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

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

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


def send_budget_details(modeladmin, request, queryset):
    queryset.update(status=2)
    for query in queryset:
        value = query.budget
        ip = "https://" + Site.objects.get_current().domain
        if value and query.status == 2:

            subject = 'Budget for ' + query.order_id + '... updated'
            message = 'Budget for ' + query.order_id + '... updated'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [query.author.email],
            contex = {'first_name': query.author.first_name, 'order_id': query.order_id, 'budget': query.budget,
                      'SITE_URL': ip, 'uuid': query.uuid}
            htmly = render_to_string('homework_help/mail-templates/budget_for_order_added.html',
                                     context=contex, request=None)
            html_message = htmly
            # html_message = "Hello " + self.author.first_name + ",<br>Budget for your order " + self.order_id + " has been updated. Your budget is " + str(self.budget) + ".<br><a href=" + ip + reverse('homework_help:order-detail-view', kwargs={'uuid': self.uuid}) + "> click here to check budget.</a> "
            mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)

            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)

def send_answer_posted(modeladmin, request, queryset):
    queryset.update(status=4)
    for query in queryset:
        ip = "https://" + Site.objects.get_current().domain

        if query.status == 4:

            subject = 'Answer for ' + query.order_id + '... updated'
            message = 'Answer for ' + query.order_id + '... updated'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [query.author.email],
            contex = {'first_name': query.author.first_name, 'order_id': query.order_id,
                      'SITE_URL': ip, 'uuid': query.uuid }
            htmly = render_to_string('homework_help/mail-templates/answer_for_order_added.html',
                                     context=contex, request=None)
            html_message = htmly
            # html_message = "Hello " + self.author.first_name + ",<br>Answer for your order " + self.order_id + " has been updated.<br><a href=" + ip + reverse('homework_help:order-detail-view', kwargs={'uuid': self.uuid}) + "> click here to check answer.</a> "
            mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)

            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)


send_budget_details.short_description = 'Send Budget Details'
send_answer_posted.short_description = 'Send Answer Notification'


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'uuid', 'order_id']
    search_fields = ['uuid', 'order_id']
    list_display = ['order_id', 'status', 'created', 'is_paid', ]
    raw_id_fields = ['question', 'author']
    actions = [send_budget_details,send_answer_posted]


class QuestionFileAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'unique_id']
    raw_id_fields = ['question', 'author']


class AnswerFileAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'unique_id']
    raw_id_fields = ['answer', 'author']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionFile, QuestionFileAdmin)
admin.site.register(AnswerFile, AnswerFileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Answers, AnswerAdmin)

