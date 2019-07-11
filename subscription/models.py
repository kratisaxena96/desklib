from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from documents.models import Document
# Create your models here.

class Plan(models.Model):
    package_name = models.CharField(_('Package Name'), db_index=True, max_length=200)
    download_limit = models.IntegerField(_('Download Limit'), blank=True, null=True)
    view_limit = models.IntegerField(_('View Limit'), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='plans', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.package_name

class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    is_current = models.BooleanField(default=True)
    expire_on = models.DateTimeField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='subscriptions')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan.package_name

class Download(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null= True, related_name='users')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document.title









