import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from subjects.models import Subject
from django.utils import timezone
from django.conf import settings
from documents.models import Document

# Create your models here.



def upload_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'upload/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )


class UploadForDocument(models.Model):
    required_document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name='upload_for_required_document', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_upload_document', blank=True, null=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    is_verified = models.BooleanField(_('Is verified'), default=False)
    is_rejected = models.BooleanField(_('Is rejected'), default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('upload for document')
        verbose_name_plural = _('uploads for document')

    def __str__(self):
        return self.required_document.title


class Upload(models.Model):
    NOTES = 1
    STUDY_MATERIAL = 2
    ASSIGNMENT_BRIEF = 3
    BOOK = 4
    JOURNAL = 5
    SOLUTION = 6
    PRESENTATION = 7
    THESIS = 8
    RESEARCH_PAPER = 9

    TYPE_OF_DOCUMENT = (
        (NOTES, 'Notes'),
        (STUDY_MATERIAL, 'Study Material'),
        (ASSIGNMENT_BRIEF, 'Assignment Brief'),
        (BOOK, 'Book'),
        (JOURNAL, 'Journal'),
        (SOLUTION, 'Solution'),
        (PRESENTATION, 'Presentation'),
        (THESIS, 'Thesis'),
        (RESEARCH_PAPER, 'Research Paper')
    )

    PENDING = 1
    ACCEPTED = 2
    REJECTED = 7

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    course_name = models.CharField(_('Course Name'), db_index=True, max_length=200)
    course_code = models.CharField(_('Course Code'), max_length=100, blank=True, null=True)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    university = models.CharField(_('University / College'), max_length=50, blank=True, null=True)
    type = models.IntegerField(choices=TYPE_OF_DOCUMENT, default=SOLUTION, db_index=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, db_index=True, related_name='subject_uploads')
    upload_file = models.FileField(verbose_name=_(' Upload File'), upload_to=upload_to, max_length=1000, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_upload', blank=True, null=True)
    # required_document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name='required_document', blank=True, null=True)
    upload_for_document = models.ForeignKey(UploadForDocument, related_name='upload_for_document', on_delete=models.CASCADE, null=True, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    is_published = models.BooleanField(_('Is published'), default=True)
    is_verified = models.BooleanField(_('Is verified'), default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('upload')
        verbose_name_plural = _('uploads')

    def __str__(self):
        return self.course_name


