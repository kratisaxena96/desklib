from django.contrib import admin
from subscription.models import Plan, Subscription, Download
# Register your models here.

admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Download)

