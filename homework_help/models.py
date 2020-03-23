import random
import string
import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from subjects.models import Subject
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify


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


def upload_question_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'homework_help/question/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )


def upload_solutions(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'solution/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )


class Question(models.Model):
    question = models.TextField(_('Question'))
    slug = models.SlugField(_('Slug'), unique=True)
    # upload_file = models.FileField(verbose_name=_('Upload File'), upload_to=upload_to, max_length=1000)
    subjects = models.ForeignKey(Subject, db_index=True, blank=True, null=True, related_name='subject_question',
                                 on_delete=models.PROTECT, )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_question')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    is_published = models.BooleanField(_('Is Published'), default=True)
    is_visible = models.BooleanField(_('Is Visible'), default=True)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        value = self.question
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class QuestionFile(models.Model):
    """
    File attached to a Question.
    """

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField(_('title'), max_length=500)
    # slug = models.SlugField(prepopulate_from=("title",))
    file = models.FileField(verbose_name=_('Question File'), upload_to=upload_question_to, max_length=1000)
    question = models.ForeignKey(Question, related_name='user_questionfiles', on_delete=models.CASCADE, null=True, blank=True)
    # visible = models.BooleanField(default=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #  Manager
    # objects = ImageManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return os.path.join(settings.MEDIA_URL,  self.file.url)
        return self.file.url

    """
    def save(self, *args, **kwargs):
        # If no album is given, add image to default album.
        super(File, self).save(*args, **kwargs)
    """

    def save(self, *args, **kwargs):
        # ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(QuestionFile, self).save(*args, **kwargs)


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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    is_accepted = models.BooleanField(_('Is Accepted'), default=False)
    is_detailed = models.BooleanField(_('Is Detailed'), default=False)
    is_paid = models.BooleanField(_('Is Published'), default=False)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id



class Answers(models.Model):
    question = models.ForeignKey(Question, related_name='answer_question', on_delete=models.PROTECT)
    solution = models.TextField(_('Solution'))
    solution_files = models.FileField(verbose_name=_('Upload File'), upload_to=upload_solutions, max_length=1000)
    answer_id = models.CharField(unique=True, max_length=10, default=key_generator, editable=False)

    is_concise = models.BooleanField(_('Is Concise'), default=False)
    is_detailed = models.BooleanField(_('Is Detailed'), default=False)
    is_published = models.BooleanField(_('Is Published'), default=False)
    is_visible = models.BooleanField(_('Is Visible'), default=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_answer',
                               blank=True, null=True)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer_id

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class Comment(models.Model):
    message = models.TextField(_('Message'))
    reference_files = models.FileField(_('Reference File'), upload_to=upload_to, blank=True, null=True,
                                       validators=[
                                           FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comment_author')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='comment_author')

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
