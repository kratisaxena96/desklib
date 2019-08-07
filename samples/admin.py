from django.contrib import admin
from samples.models import Sample, Image

# Register your models here.

class ImageInline(admin.TabularInline):
    raw_id_fields = ('sample',)
    # readonly_fields = ('author',)
    exclude = ['author']
    model = Image


class SampleAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'published_date'
    raw_id_fields = ('author',)
    search_fields = ['name',]
    list_display = ('name','published_date','is_published', )

    inlines = [
        ImageInline
    ]

admin.site.register(Sample, SampleAdmin)

