import random
import string

from django.conf import settings
from django.db import models
from django.utils import timezone
from subjects.models import Subject
from django.utils.translation import ugettext_lazy as _


# Create your models here.

def key_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def upload_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'homework_help/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )


class Question(models.Model):
    question = models.TextField(_('Question'))
    slug = models.SlugField(_('Slug'), unique=True)
    upload_file = models.FileField(verbose_name=_('Upload File'), upload_to=upload_to, max_length=1000)
    subjects = models.ForeignKey(Subject, db_index=True, blank=True, null=True, related_name='subject_question', on_delete=models.PROTECT,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_question',
                               blank=True, null=True)

    is_published = models.BooleanField(_('Is Published'), default=True)
    is_visible = models.BooleanField(_('Is Visible'), default=True)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class Order(models.Model):
    STATUS_UNASSIGNED = 1
    STATUS_IN_PROGRESS = 2
    STATUS_DONE = 3
    STATUS_DELIVERED = 4
    STATUS_FEEDBACK = 5
    STATUS_CANCELLED = 6

    STATUS = [
    (STATUS_UNASSIGNED, 'Unassigned'),
    (STATUS_IN_PROGRESS, 'In Progress'),
    (STATUS_DONE, 'Completed'),
    (STATUS_DELIVERED, 'Delivered'),
    (STATUS_FEEDBACK, 'Feedback'),
    (STATUS_CANCELLED, 'Cancelled'),
    ]

    question = models.ForeignKey(Question, related_name='ordered_question', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_order')
    status = models.IntegerField(choices=STATUS, default=STATUS_UNASSIGNED, db_index=True)
    remarks = models.TextField(_('Remarks'), null=True, blank=True)
    budget = models.IntegerField(_('Budget'), null=True, blank=True)
    amount_paid = models.IntegerField(_('Amount Paid'), null=True, blank=True)
    order_id = models.CharField(unique=True, max_length=10, default=key_generator, editable=False)
    uuid = models.CharField(unique=True, max_length=10, default=key_generator, editable=False)

    is_accepted = models.BooleanField(_('Is Accepted'), default=False)
    is_paid = models.BooleanField(_('Is Published'), default=False)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id


class Comment(models.Model):
    message = models.TextField(_('Message'))
    reference_files = models.FileField(_('Reference File'), upload_to=upload_to, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comment_author')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='comment_author')

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
