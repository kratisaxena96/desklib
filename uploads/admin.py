from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives

from documents.models import Document
from subscription.models import PayPerDocument, Plan
from uploads.models import Upload, UploadForDocument
from datetime import timedelta
from django.conf import settings
from datetime import datetime
from django.template.loader import render_to_string
from subjects.models import Subject
from django.contrib.sites.models import Site

# Register your models here.


# class SubjectListFilter(admin.SimpleListFilter):
#     title = 'Subjects'
#     parameter_name = 'sub'
#     default_value = None
#
#     def lookups(self, request, model_admin):
#         list_of_subjects = []
#         queryset = Subject.objects.all()
#         for sub in queryset:
#             list_of_subjects.append(
#                 (str(sub.id), sub.name)
#             )
#         return sorted(list_of_subjects, key=lambda tp: tp[1])
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(subjects__id=int(self.value()))
#         return queryset


# def make_verified(modeladmin, request, queryset):
#     queryset.update(is_verified=True)
#
# make_verified.short_description = "Mark selected document is verified"


def make_subscription(modeladmin, request, queryset):
    for document in queryset:
        doc = document.required_document.slug
        if (document.is_verified==True):
            user = document.author
            plan = Plan.objects.get(is_pay_per_download=True)
            create = PayPerDocument.objects.create(user=user, expire_on=datetime.now() + timedelta(days=30),
                                                   plan=plan, start_date=datetime.now())
            create.documents.add(document.required_document)
            site_url = Site.objects.get_current().domain
            context = {'document': document.required_document, 'user': user, 'SITE_URL': site_url}
            htmly = render_to_string('subscription/mail-templates/v2/make_subscription.html',
                                     context=context, request=None)
            html_message = htmly
            mail = EmailMultiAlternatives(
                subject='Regarding your requested document',
                to=[user.email],
                body=''
            )
            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)

        elif(document.is_rejected==True):
            user = document.author
            site_url = Site.objects.get_current().domain
            context = {'document': document.required_document, 'user': user, 'SITE_URL': site_url}
            htmly = render_to_string('subscription/mail-templates/v2/uploads_rejected_email.html',
                                     context=context, request=None)
            html_message = htmly
            mail = EmailMultiAlternatives(
                subject='Regarding the rejection of your uploaded files',
                to=[user.email],
                body=''
            )
            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)

        else:
            pass


make_subscription.short_description = "Make Pay Per Subscription or Reject"


class UploadInlineAdmin(admin.TabularInline):
    # form = SampleFileAdminForm
    model = Upload
    extra = 1

    exclude = ['course_name', 'course_code', 'country', 'university', 'type', 'is_published']
    raw_id_fields = ('author', 'subjects')


class UploadForDocumentAdmin(admin.ModelAdmin):
    inlines =[UploadInlineAdmin]
    raw_id_fields = ['required_document', 'author']
    readonly_fields = ('created', 'updated')
    actions = [make_subscription]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('uploads.create_or_reject_pay_per_subscription'):
            del actions['make_subscription']
        return actions

class UplaodAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'unique_id')
    raw_id_fields = ('author','subjects','author')
    search_fields = ['course_name', 'university']
    list_display = ('course_name', 'type', 'is_published', 'get_subjects')
    list_filter = ('subjects', 'type', 'is_published')

    def get_subjects(self, obj):
        return "\n".join([sub.name for sub in obj.subjects.all()])

admin.site.register(Upload, UplaodAdmin)
admin.site.register(UploadForDocument, UploadForDocumentAdmin)