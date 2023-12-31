import os
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from taggit.managers import TaggableManager
from django.urls import reverse
from meta.models import ModelMeta
from ckeditor_uploader.fields import RichTextUploadingField


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/subject/', filename)


class Subject(ModelMeta, models.Model):
    name = models.CharField(_('Title'), db_index=True, max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    # keywords = models.CharField(_('Keywords'), max_length=1000, blank=True, null=True,)
    parent_subject = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, verbose_name="Parent Subject")
    description = models.TextField(_('Description'), max_length=2000, blank=True, null=True, )
    parent_question_description = models.TextField(_('Parent Question description'), null=True, blank=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='PROTECT', related_name='author_document')
    keywords = TaggableManager(blank=True)

    is_parent = models.BooleanField(default=False)
    introduction = models.TextField(_('Introduction'), max_length=2000, null=True, blank=True)
    short_description = models.TextField(_('Short description'), max_length=500, null=True, blank=True)
    sub_heading = models.CharField(_('Sub heading'), max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to=get_file_path, help_text='Image of the subject', null=True, blank=True)
    image_alt_text = models.CharField(max_length=70, help_text='Alternate text of subject image', null=True, blank=True)
    info_graphic_image = models.ImageField(upload_to=get_file_path, help_text='Graphic image of the parent subject', null=True, blank=True)
    info_graphic_image_alt_text = models.CharField(max_length=70, help_text='Alternate text of parent subject graphic image', null=True, blank=True)

    blog_title = models.CharField(_('Blog Title'), max_length=200, null=True, blank=True)

    seo_title = models.CharField(max_length=150, help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.', null=True, blank=True)
    seo_description = models.TextField(max_length=500, help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.', null=True, blank=True)
    seo_keywords = models.CharField(max_length=500, help_text='Recommended max.length of relevant seo keyword is 140 characters', null=True, blank=True)
    study_short_description = models.TextField(null=True, blank=True)

    canonical_url = models.URLField(max_length=2048, blank=True, null=True, help_text='Search Engine like max. 2048 characters of url')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False, related_name='subject_user', null=True, blank=True)
    last_edited = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False, related_name='subject_last_edited', null=True, blank=True)
    is_visible = models.BooleanField(_('Is visible'), default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    _metadata = {
            'use_og': 'True',
            'use_facebook': 'True',
            'use_twitter': 'True',
            'use_title_tag': 'False',
            'use_googleplus': 'True',
            'use_sites': 'True',
            'keywords': 'seo_keywords',
            'title': 'seo_title',
            'description': 'seo_description',
            'canonical_url': 'canonical_url',
        }


    @property
    def sd(self):
        return {
            "@type": 'Document',
            "description": self.title,
            "name": self.title,
        }

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')

    def __str__(self):
        return self.name

    def get_keywords(self):
        keywords = self.seo_keywords.split(",")
        return keywords

    def get_absolute_url(self):
        if self.parent_subject:
            return reverse('subjects:child-subject-view', kwargs={'parent_subject': self.parent_subject.slug, 'slug': self.slug})
        else:
            return reverse('subjects:parent-subject-view', kwargs={'slug': self.slug})


class SubjectContent(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_content')
    title = models.CharField(_('Title'), max_length=500)
    slug = models.SlugField(_('Slug'), unique=True)
    description = RichTextUploadingField(_('Description'))

    class Meta:
        verbose_name = _('subject content')
        verbose_name_plural = _('subject content')

    def __str__(self):
        return self.title


class SubjectQuestionContent(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_question_content')
    title = models.CharField(_('Title'), max_length=500)
    slug = models.SlugField(_('Slug'), unique=True)
    description = RichTextUploadingField(_('Description'))

    class Meta:
        verbose_name = _('subject question content')
        verbose_name_plural = _('subject question content')

    def __str__(self):
        return self.title