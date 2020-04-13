from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from meta.models import ModelMeta
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.


class BlogCategoryModel(ModelMeta, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover_page = models.ImageField(blank=True, null=True, upload_to='blog_cat/%Y/%m/%D')

    seo_title = models.CharField(max_length=70, null=True)
    seo_description = models.TextField(max_length=160, null=True)
    seo_keywords = models.CharField(max_length=140, null=True)

    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')

    _metadata = {
        'keywords': 'get_keywords',
        'title': 'seo_title',
        'description': 'seo_description',
    }

    @property
    def sd(self):
        return {
            "@type": 'Website',
            "name": self.name,
        }

    def get_keywords(self):
        keywords = self.seo_keywords.split(",")
        return keywords


class BlogModel(ModelMeta,models.Model):

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(blank=True, null=True, upload_to="photos")
    # category = models.CharField(_('Category'), max_length=100, choices=CATEGORY, blank=True, null=True)
    category = models.ManyToManyField(BlogCategoryModel, max_length=100, blank=True, null=True, related_name='category_blog')
    short_description = models.TextField(max_length=200, blank=True, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    author = models.CharField(max_length=20, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='blog_author')

    is_published = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    published_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    seo_title = models.CharField(max_length=70, null=True)
    seo_description = models.TextField(max_length=160, null=True)
    seo_keywords = models.CharField(max_length=140, null=True)

    _metadata = {
        'keywords': 'get_keywords',
        'title': 'seo_title',
        'description': 'seo_description',
    }

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def __str__(self):
        return self.title


    def get_keywords(self):
        keywords = self.seo_keywords.split(",")
        return keywords

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'year': self.published_date.year, 'month': self.published_date.month, 'date': self.published_date.day, 'slug': self.slug})

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    @property
    def sd(self):
        return {
            "@type": 'Website',
            "description": self.description,
            "name": self.title,
        }
