from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Create your models here.


class Review(models.Model):
    stars = models.IntegerField(max_length=5)
    review = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_review',
                               blank=True, null=True)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['created_at', ]

    def __str__(self):
        return self.stars
