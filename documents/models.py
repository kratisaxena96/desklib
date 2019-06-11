import os
import tempfile

from django.db import models
from documents.utils import key_generator, get_text
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone



# Create your models here.

def upload_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'document/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )


class Subject(models.Model):
    name = models.CharField(max_length=100)
    # timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')

    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('college')
        verbose_name_plural = _('colleges')

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete='PROTECT', related_name="college_course")
    subject = models.ForeignKey(Subject, on_delete='PROTECT', related_name="subject_course")
    semester = models.IntegerField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True                                      )

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.title


class Document(models.Model):
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

    key = models.CharField(db_index=True, unique=True, max_length=10, default=key_generator, editable=False)
    title = models.CharField(_('Title'), db_index=True, max_length=200)
    slug = models.SlugField(_('Slug'),unique=True )
    type = models.IntegerField(choices=TYPE_OF_DOCUMENT, default=SOLUTION)
    subject = models.ForeignKey(Subject,db_index=True, on_delete='SET_NULL',blank=True, null=True, related_name='subject_document')
    college = models.ForeignKey(College, db_index=True, on_delete='SET_NULL',blank=True, null=True,  related_name='college_document')
    course = models.ForeignKey(Course, db_index=True, on_delete='SET_NULL', blank=True, null=True, related_name='course_code_document')
    keywords = models.CharField(_('Keywords'), max_length=1000, blank=True, null=True,)
    description = RichTextField(_('Description'), blank=True, null=True)
    content = models.TextField(_('Content'), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='PROTECT', related_name='author_document')
    summary = models.TextField(_('Summary'), blank=True, null=True)
    initial_text = models.TextField(_('Initial Text'), blank=True, null=True)
    first_sentence = models.CharField(_('First Sentence'), max_length=1000)
    file = models.FileField(verbose_name=_('File'), upload_to=upload_to, max_length=1000)

    is_published = models.BooleanField(_('Is Published'), default=False)
    is_visible = models.BooleanField(_('Is Visible'), default=False)

    published_date = models.DateTimeField(_('Published Date'))
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # Get the complete file path to obtain filename
        filename = self.file.name
        filename = os.path.basename(filename)

        f1 = self.file.file  # File to copy from
        temp = tempfile.NamedTemporaryFile(suffix=filename)  # File to copy to
        # Copying file contents
        with open(temp.name, 'wb') as f2:
            f2.write(f1.read())

        f2.close()
        # Extracting text
        text = get_text(temp.name)
        self.content = text

        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(Document, self).save(*args, **kwargs)
