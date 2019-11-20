from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Create your models here.


class Review(models.Model):
    stars = models.IntegerField(max_length=5)
    description = models.TextField(max_length=500)
    title = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['created_at', ]

    def __str__(self):
        return self.title
