from django.contrib import admin
from samples.models import Sample, Image

# Register your models here.


def soft_delete_samples(modeladmin, request, queryset):
    for sample in queryset:
        if sample.is_published == True or sample.is_visible == True:
            sample.is_published = False
            sample.is_visible = False
            sample.save()


soft_delete_samples.short_description = 'Soft Delete Samples'


def restore_samples(modeladmin, request, queryset):
    for sample in queryset:
        if sample.is_published == False or sample.is_visible == False:
            sample.is_published = True
            sample.is_visible = True
            sample.save()


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

