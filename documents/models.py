import os
import tempfile
import datetime
import tempfile


from django.db import models
from documents.utils import key_generator, get_text, get_title, get_summary, get_sentences_from_text, get_first_sentence
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from pdf2image.exceptions import (PDFInfoNotInstalledError,PDFPageCountError,PDFSyntaxError)
from pdf2image import convert_from_path, convert_from_bytes
from meta.models import ModelMeta
from django.urls import reverse




# Create your models here.
from subjects.models import Subject
from subjects.utils import get_subjects


def upload_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'document/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )

def all_files(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'files/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )

def main_files(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'main_files/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )

def pdf_converted_files(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'pdf_converted_file/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )

def images(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'images/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )





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
    # subject = models.ForeignKey(Subject, on_delete='PROTECT', related_name="subject_course")
    semester = models.IntegerField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    def __str__(self):
        return self.title


class Document(ModelMeta, models.Model):
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
    type = models.IntegerField(choices=TYPE_OF_DOCUMENT, default=SOLUTION, db_index=True)
    subjects = models.ManyToManyField(Subject, db_index=True, blank=True, null=True, related_name='subject_documents')
    college = models.ForeignKey(College, db_index=True, on_delete='SET_NULL',blank=True, null=True,  related_name='college_documents')
    course = models.ForeignKey(Course, db_index=True, on_delete='SET_NULL', blank=True, null=True, related_name='course_code_documents')
    keywords = models.CharField(_('Keywords'), max_length=1000, blank=True, null=True,)
    description = RichTextField(_('Description'), blank=True, null=True)
    content = models.TextField(_('Content'), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='PROTECT', related_name='author_document' ,blank=True, null=True)
    summary = models.TextField(_('Summary'), blank=True, null=True)
    initial_text = models.TextField(_('Initial Text'), blank=True, null=True)
    first_sentence = models.CharField(_('First Sentence'), max_length=1000 ,blank=True, null=True)
    upload_file = models.FileField(verbose_name=_('Upload File'), upload_to=upload_to, max_length=1000)
    main_file = models.FileField(verbose_name=_(' Main File'), upload_to=main_files, max_length=1000, blank=True, null=True)
    pdf_converted_file = models.FileField(verbose_name=_(' Pdf converted file'), upload_to=pdf_converted_files, max_length=1000,blank=True, null=True)
    words = models.IntegerField(_('Total Words'), blank=True, null=True)
    page = models.IntegerField(_('Total pages'), blank=True, null=True)
    filename = models.CharField(_('Title'), max_length=200, blank=True, null=True)


    is_published = models.BooleanField(_('Is Published'), default=False)
    is_visible = models.BooleanField(_('Is Visible'), default=False)

    published_date = models.DateTimeField(_('Published Date'),blank=True, null=True)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    seo_title = models.CharField(max_length=70,
                                 help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.')
    seo_description = models.TextField(max_length=160,
                                       help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.')
    seo_keywords = models.CharField(max_length=140,
                                    help_text='Recommended max.length of relevant seo keyword is 140 characters')


    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # Get the complete file path to obtain filename

        # First time save
        filename = self.upload_file.name
        filename = os.path.basename(filename)

        f1 = self.upload_file.file  # File to copy from
        temp = tempfile.NamedTemporaryFile(suffix=filename)  # File to copy to
        # Copying file contents
        with open(temp.name, 'wb') as f2:
            f2.write(f1.read())

        f2.close()

        # Extracting text
        text = get_text(temp.name)
        self.content = text
        self.description = text
        title = get_title(text)
        self.title = title
        self.slug = slugify(self.title)

        # self.summary = get_summary
        sentences = get_sentences_from_text(text)
        summary_list = get_summary(sentences)
        if not self.summary:
            for summary in summary_list:
                self.summary += summary
                self.initial_text += summary

        self.first_sentence = get_first_sentence(sentences)
        self.published_date = datetime.datetime.now() + datetime.timedelta(+30)

        if not self.id:
            self.created = timezone.now()

        self.author = User.objects.first()
        self.updated = timezone.now()
        # self.subjects.set(get_subjects(text))

        # convert the uploaded file to pdf file and save it
        try:
            os.system('libreoffice --headless --convert-to pdf --outdir /tmp '+ temp.name)
            file_without_ext = os.path.splitext(filename)[0]
            file_with_pdf_ext = file_without_ext +".pdf"

            pdf_converted_loc = os.path.splitext(temp.name)
            pdf_converted_loc = pdf_converted_loc[0] + ".pdf"

            f = open(pdf_converted_loc, 'rb')
            myfile = DjangoFile(f)
            self.pdf_converted_file = myfile
            self.pdf_converted_file.name = file_with_pdf_ext

            os.system('mkdir /tmp/'+file_without_ext)
            pdf_images = convert_from_path(pdf_converted_loc, output_folder='/tmp/'+file_without_ext, fmt='jpg')

            for subject in get_subjects(text):
                self.subjects.add(subject)

            super(Document, self).save(*args, **kwargs)

            for pdf_img in pdf_images:
                print(pdf_img)
                image = Image()
                image.image_file = pdf_img.filename
                image.document = self
                image.author = self.author
                image.save()
        except:
            super(Document, self).save(*args, **kwargs)
            print("An exception >>>>>>>>>>>>>>>>>>>>>>>>> occurred")

    _metadata = {
            'use_og': 'True',
            'use_facebook': 'True',
            'use_twitter': 'True',
            'use_title_tag': 'True',
            'use_googleplus': 'True',
            'use_sites': 'True',
            'keywords': 'seo_keywords',
            'title': 'seo_title',
            'description': 'seo_description',
            'canonical_url': 'canonical_url',
            # 'image': settings.DEFAULT_IMAGE,
            # 'object_type': 'settings.DEFAULT_TYPE',
            # 'og_type': 'settings.FB_TYPE',
            # 'og_app_id': 'settings.FB_APPID',
            # 'og_profile_id': 'settings.FB_PROFILE_ID',
            # 'og_publisher': 'settings.FB_PUBLISHER',
            # 'og_author_url': 'settings.FB_AUTHOR_URL',
            # 'fb_pages': 'settings.FB_PAGES',
            # 'twitter_type': 'settings.TWITTER_TYPE',
            # 'twitter_site': 'settings.TWITTER_SITE',
            # 'twitter_author': 'settings.TWITTER_AUTHOR',
            # 'gplus_type': 'settings.GPLUS_TYPE',
            # 'gplus_author': 'settings.GPLUS_AUTHOR',
            # 'gplus_publisher': 'settings.GPLUS_PUBLISHER',
        }

    def get_absolute_url(self):
        return reverse('documents:document-view', args=[str(self.slug)])


class File(models.Model):
    """Unit of work to be done."""
    key = models.CharField(unique=True, max_length=10, default=key_generator, editable=False)
    file = models.FileField(verbose_name=_('File'), upload_to=all_files, max_length=1000 )
    document = models.ForeignKey(Document, blank=True, null=True, on_delete='SET_NULL', related_name='document_file')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='SET_NULL', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    image_file = models.ImageField(verbose_name=_('Image'), upload_to=images, max_length=1000 )
    document = models.ForeignKey(Document, blank=True, null=True, on_delete='SET_NULL', related_name='document_image')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='SET_NULL', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
