from django.contrib import admin
from samples.models import Sample, Image

# Register your models here.


def soft_delete_samples(modeladmin, request, queryset):
    queryset.update(is_published = False, is_visible = False)


soft_delete_samples.short_description = 'Soft Delete Samples'


def restore_samples(modeladmin, request, queryset):
    queryset.update(is_published = True, is_visible = True)


restore_samples.short_description = 'Restore Samples'


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
    list_display = ('name','published_date','is_published', 'is_visible', )
    actions = [soft_delete_samples, restore_samples]

    inlines = [
        ImageInline
    ]

admin.site.register(Sample, SampleAdmin)

