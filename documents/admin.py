from django.contrib import admin
from documents.models import Document, File, Image



# Register your models here.

class FileInline(admin.TabularInline):
    model = File

class ImageInline(admin.TabularInline):
    model = Image

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'key')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        FileInline,
        ImageInline
    ]





admin.site.register(Document, DocumentAdmin)