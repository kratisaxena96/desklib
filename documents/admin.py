import os

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from post_office.admin import EmailAdmin
from post_office.models import Email

from documents.admin_forms import PublishedDateForm, ChangeAuthorForm, DocumentAdminForm
from documents.models import Document, File, Page, Report, Issue
from subjects.models import Subject
from django.db.models import F
from subjects.utils import get_subjects
from django.template.response import TemplateResponse
from accounts.models import UserAccount
from django.contrib.auth.models import Permission
from django.contrib import admin
admin.site.register(Permission)


def publish_documents(modeladmin, request, queryset):
    queryset.update(is_published = True)


publish_documents.short_description = 'Publish Documents'

def visble_documents(modeladmin, request, queryset):
    queryset.update(is_visible = True)


visble_documents.short_description = 'Visible Documents'

def chage_publish_date(modeladmin, request, queryset):
    if 'date_time_1' and 'date_time_0' in request.POST:
        str = request.POST.get('date_time_0')+' '+request.POST.get('date_time_1')
        queryset.update(published_date=str)
        messages.info(request, 'Publish Date changed of'" %s"%queryset.count()+' documents')
        return HttpResponseRedirect(request.get_full_path())
    else:
        form = PublishedDateForm()
        return TemplateResponse(request,"admin/change_published_date.html", context={'dates_obj':queryset, 'form': form})


chage_publish_date.short_description = 'Change Publish Date'

def change_author(modeladmin, request, queryset):
    user_id = request.POST.get('user')
    if user_id:
        user = UserAccount.objects.get(id = user_id)
        queryset.update(author=user)
        messages.add_message(request, messages.INFO, 'Author of "%s" Documents has been updated'%(queryset.count()))
        return HttpResponseRedirect(request.get_full_path())
    else:
        form = ChangeAuthorForm(user=request.user)
        return TemplateResponse(request, "admin/change_author_documents.html", context={'author_obj':queryset,'form': form})
change_author.short_description = 'Change Author'


def un_publish_documents(modeladmin, request, queryset):
    queryset.update(is_published = False)


un_publish_documents.short_description = 'Un-Publish Documents'


def soft_delete_documents(modeladmin, request, queryset):
    queryset.update(is_published = False, is_visible = False)


soft_delete_documents.short_description = 'Soft Delete Documents'

def hard_delete_documents(modeladmin, request, queryset):
    for document in queryset:
        if document.upload_file:
            if os.path.isfile(document.upload_file.path):
                os.remove(document.upload_file.path)
        if document.main_file:
            if os.path.isfile(document.main_file.path):
                os.remove(document.main_file.path)
        for page in document.pages.all():
            if os.path.isfile(page.image_file.path):
                os.remove(page.image_file.path)
        for file in document.document_file.all():
            if os.path.isfile(file.file.path):
                os.remove(file.file.path)
        document.delete()

hard_delete_documents.short_description = 'Hard Delete Documents with assets'

def restore_documents(modeladmin, request, queryset):
    queryset.update(is_published = True, is_visible = True)


restore_documents.short_description = 'Restore Documents'


def set_document_subject(modeladmin, request, queryset):
    for doc in queryset:
        for subject in get_subjects(doc.description):
            doc.subjects.add(subject)


set_document_subject.short_description = 'Set Subjects of Documents'


class SubjectListFilter(admin.SimpleListFilter):
    title = 'Subjects'
    parameter_name = 'sub'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_subjects = []
        queryset = Subject.objects.all()
        for sub in queryset:
            list_of_subjects.append(
                (str(sub.id), sub.name)
            )
        return sorted(list_of_subjects, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subjects__id=int(self.value()))
        return queryset

class EmployeeListFilter(admin.SimpleListFilter):
    title = 'employee'
    parameter_name = 'emp'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_authors = []
        queryset = UserAccount.objects.filter(is_staff=True, is_active=True)
        for auth in queryset:
            list_of_authors.append(
                (str(auth.id), auth.username)
            )
        return sorted(list_of_authors, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__id=int(self.value()))
        return queryset
#
# class ByAuthorFilter(admin.SimpleListFilter):
#     title = 'Author'
#     parameter_name = 'author'
#     default_value = None
#
#     def lookups(self, request, model_admin):
#         list_of_authors = []
#         queryset = UserAccount.objects.filter(is_staff=True, is_superuser=False)
#         for author in queryset:
#             list_of_authors.append(
#                 (str(author.username))
#             )
#         return list_of_authors
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(username=self.value())
#         return queryset

class FileInline(admin.TabularInline):
    raw_id_fields = ('document',)
    # readonly_fields = ('author',)
    exclude = ['author']
    model = File


class PageInline(admin.TabularInline):
    raw_id_fields = ('document',)
    # readonly_fields = ('author',)
    exclude = ['author']
    model = Page

def sendmail(modeladmin, request, queryset):
    """An admin action to send  emails on priority"""

    for query in queryset:
        query.dispatch()

sendmail.short_description = 'Send Mail'

admin.site._registry[Email].actions.append(sendmail)


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'key')
    # prepopulated_fields = {'slug': ('title',)}
    form = DocumentAdminForm
    date_hierarchy = 'published_date'
    raw_id_fields = ('author','subjects')
    search_fields = ['title', 'content','slug','upload_file']
    list_display = ('title', 'published_date', 'is_published', 'is_visible', 'page', 'words', 'get_subjects')
    list_filter = (SubjectListFilter, 'is_published', 'is_visible' , EmployeeListFilter)
    actions = [publish_documents, un_publish_documents, visble_documents, soft_delete_documents, set_document_subject, restore_documents, hard_delete_documents, chage_publish_date, change_author]

    inlines = [
        FileInline,
        PageInline
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('documents.change_document_author'):
            del actions['change_author']
        return actions

    def get_queryset(self, request):
        qs = super(DocumentAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('documents.change_document_author'):
            return qs
        return qs.filter(author=request.user)

    def get_subjects(self, obj):
        return "\n".join([sub.name for sub in obj.subjects.all()])

    def get_queryset(self, request):
        queryset = super(DocumentAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('pages').prefetch_related('document_file').prefetch_related(
            'pages__author').prefetch_related('document_file__author')
        if request.user.is_superuser  or request.user.has_perm('documents.change_document_author'):
            return queryset
        return queryset.filter(author=request.user)

    def get_form(self, request, obj=None, **kwargs):
        # Proper kwargs are form, fields, exclude, formfield_callback
        if obj:  # obj is not None, so this is a change page
            pass
        else:  # obj is None, so this is an add page
            kwargs['exclude'] = (
            'title', 'slug', 'subjects', 'key', 'created', 'updated', 'seo_title', 'seo_description', 'seo_keywords',)

        return super(DocumentAdmin, self).get_form(request, obj, **kwargs)

class ReportAdmin(admin.ModelAdmin):
    raw_id_fields = ('issue','author','document')

class IssueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

            # Prevent non-superusers from editing their own permissions
        if (
                not is_superuser
                and obj is not None
                and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
admin.site.register(Document, DocumentAdmin)

admin.site.register(Issue, IssueAdmin)
admin.site.register(Report, ReportAdmin)
