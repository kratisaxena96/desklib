from django.contrib import admin
from contact.models import ContactUsModel
# Register your models here.



class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ['created', ]


admin.site.register(ContactUsModel, ContactAdmin)
