from django.contrib import admin
from documents.models import Document, File



# Register your models here.

class FileInline(admin.TabularInline):
    model = File

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'key')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        FileInline,
    ]





admin.site.register(Document, DocumentAdmin)