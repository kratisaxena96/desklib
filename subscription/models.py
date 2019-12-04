from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from documents.models import Document
from documents.utils import key_generator
# Create your models here.


class Plan(models.Model):
    key = models.CharField(db_index=True, unique=True, max_length=10, default=key_generator, editable=False)
    slug = models.SlugField(_('Slug'), unique=True)
    package_name = models.CharField(_('Package Name'), db_index=True, max_length=200)
    price = models.IntegerField(_('Price'))
    is_pay_per_download = models.BooleanField(default=False)
    download_limit = models.IntegerField(_('Download Limit'), blank=True, null=True)
    view_limit = models.IntegerField(_('View Limit'), blank=True, null=True)
    days = models.IntegerField(_('Plan Days'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='plans', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.package_name

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name = 'subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    is_current = models.BooleanField(default=True)
    expire_on = models.DateTimeField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='subscription_author')
    is_pay_per_download = models.BooleanField(default=True, blank=True, null=True,)
    documents =  models.ManyToManyField(Document, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan.package_name

class PayPerDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name = 'pay_per_download')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    documents =  models.ManyToManyField(Document, null=True, blank=True)
    is_current = models.BooleanField(default=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pay_per_doc_author')
    start_date = models.DateTimeField()
    expire_on = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Download(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null= True, related_name='users')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document.title


class PageView(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='pageviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='pageviews_users')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document.title


class SessionPageView(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='session_pageviews')
    session = models.CharField(_('Session Id'), max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document.title







