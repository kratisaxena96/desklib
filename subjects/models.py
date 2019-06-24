from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from taggit.managers import TaggableManager


class Subject(models.Model):
    name = models.CharField(_('Title'), db_index=True, max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    # keywords = models.CharField(_('Keywords'), max_length=1000, blank=True, null=True,)
    description = RichTextField(_('Description'), blank=True, null=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='PROTECT', related_name='author_document')
    keywords = TaggableManager(blank=True)

    is_visible = models.BooleanField(_('Is visible'), default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')

    def __str__(self):
        return self.name
