from django.contrib import admin
from subscription.models import Plan, Subscription, Download, PageView, SessionPageView
# Register your models here.


class DownloadAdmin(admin.ModelAdmin):
    search_fields = ['document__title', ]
    list_display = ('document', 'user', 'created_at', 'updated_at')


class PlanAdmin(admin.ModelAdmin):
    search_fields = ['package_name']
    list_display = ('package_name', 'download_limit', 'view_limit', 'author', 'created_at', 'updated_at')


class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ['plan__package_name']
    list_display = ('user', 'plan', 'is_current', 'expire_on', 'author', 'created_at', 'updated_at')


class PageViewsAdmin(admin.ModelAdmin):
    search_fields = ['document__title', ]
    list_display = ('document', 'user', 'created_at', 'updated_at')


class SessionPageViewsAdmin(admin.ModelAdmin):
    search_fields = ['document__title', ]
    list_display = ('document', 'session', 'created_at', 'updated_at')

admin.site.register(Plan,PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(PageView, PageViewsAdmin)
admin.site.register(SessionPageView, SessionPageViewsAdmin)


