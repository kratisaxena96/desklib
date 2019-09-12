import os
import re
import tempfile
import datetime
import uuid

from io import BytesIO
from sorl.thumbnail import ImageField, get_thumbnail

from django.core.files.base import ContentFile
from django.db import models
from documents.utils import key_generator, get_text, get_title, get_summary, get_sentences_from_text, \
    get_first_sentence, get_html_from_pdf_url, get_filename_from_path, get_keywords_from_text, get_words_from_text, \
    random_string_generator, unique_slug_generator
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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

    return 'files/{}'.format(
        filename,
    )

def main_files(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'files/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )

def pdf_converted_files(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'pdf/{}'.format(
        uuid.uuid4().hex+'.pdf',
    )

def images(instance, filename):
    now = timezone.now()
    file_name = get_filename_from_path(filename)
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'images/{}'.format(
        file_name,
    )

def cover_images(instance, filename):
    now = timezone.now()
    file_name = get_filename_from_path(filename)
    return 'cover-images/{}'.format(
        file_name,
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
    slug = models.SlugField(_('Slug'), unique=True)
    type = models.IntegerField(choices=TYPE_OF_DOCUMENT, default=SOLUTION, db_index=True)
    subjects = models.ManyToManyField(Subject, db_index=True, blank=True, null=True, related_name='subject_documents')
    college = models.ForeignKey(College, db_index=True, on_delete=models.SET_NULL ,blank=True, null=True,  related_name='college_documents')
    course = models.ForeignKey(Course, db_index=True, on_delete=models.SET_NULL, blank=True, null=True, related_name='course_code_documents')
    keywords = models.CharField(_('Keywords'), max_length=1000, blank=True, null=True,)
    description = RichTextField(_('Description'), blank=True, null=True)
    content = models.TextField(_('Content'), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_document' ,blank=True, null=True)
    summary = models.TextField(_('Summary'), blank=True, null=True)
    initial_text = models.TextField(_('Initial Text'), blank=True, null=True)
    first_sentence = models.CharField(_('First Sentence'), max_length=1000 ,blank=True, null=True)
    upload_file = models.FileField(verbose_name=_('Upload File'), upload_to=upload_to, max_length=1000)
    main_file = models.FileField(verbose_name=_(' Main File'), upload_to=main_files, max_length=1000, blank=True, null=True)
    # pdf_converted_file = models.FileField(verbose_name=_(' Pdf converted file'), upload_to=pdf_converted_files, max_length=1000,blank=True, null=True)
    words = models.IntegerField(_('Total Words'), blank=True, null=True)
    page = models.IntegerField(_('Total pages'), blank=True, null=True)
    filename = models.CharField(_('filename'), max_length=200, blank=True, null=True)

    was_helpful = models.IntegerField(_('Helpful'), null=True, blank=True, default=0)
    not_helpful = models.IntegerField(_('Not Helpful'), null=True, blank=True, default=0)

    preview_from = models.PositiveIntegerField(default=1)
    preview_to = models.PositiveIntegerField(default=2)
    total_downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    search_clicks = models.PositiveIntegerField(default=0)
    google_clicks = models.PositiveIntegerField(default=0)
    cover_page_number = models.PositiveIntegerField(_('Cover Page No.'), null=True, blank=True,default=0)


    is_published = models.BooleanField(_('Is Published'), default=True)
    is_visible = models.BooleanField(_('Is Visible'), default=True)
    require_recalculation = models.BooleanField(_('Require Recalculation'), default=False)

    published_date = models.DateTimeField(_('Published Date'), default=timezone.now)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    seo_title = models.CharField(max_length=70,
                                 help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.')
    seo_description = models.TextField(max_length=160,
                                       help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.')
    seo_keywords = models.CharField(max_length=140,
                                    help_text='Recommended max.length of relevant seo keyword is 140 characters')

    # cover_image = models.ImageField(verbose_name=_('Image'), upload_to=cover_images, max_length=1000, blank = True, null = True, help_text='Dimensions Should be 80x112 as per document ration')

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

    @property
    def sd(self):
        return {
            "@type": 'Document',
            "description": self.title,
            "name": self.title,
        }

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # Get the complete file path to obtain filename

        # First time save
        if not kwargs.get('ignore_timestamps'):
            self.updated = timezone.now()

        # We only autogenerate data at time of creation.
        if not self.id or self.require_recalculation:
            # Populating created timestamp
            self.created = timezone.now()
            # Generating filename without spaces. Replacing them with underscore.
            filename = self.upload_file.name
            filename = os.path.basename(filename)
            filename = filename.replace(' ', '_')

            f1 = self.upload_file.file  # File to copy from
            temp = tempfile.NamedTemporaryFile(suffix=filename)  # Temporary File to copy to
            # Copying file contents
            with open(temp.name, 'wb') as f2:
                f2.write(f1.read())

            f2.close()

            # Extracting text from file
            text = get_text(temp.name)
            self.content = text
            self.description = text
            title = get_title(text)
            self.title = title
            # Generating slug. This will check for existing slugs and generate unique slug.
            # self.slug = slugify(self.title)
            # rand_str = random_string_generator()
            # strtime = "".join(str(time()).split("."))
            # string = "%s-%s" % (self.title[:20], rand_str)

            self.slug = unique_slug_generator(self, new_slug=slugify(self.title[:40]) if self.title else random_string_generator(size=4))

            self.words = len(get_words_from_text(text))


            # self.summary = get_summary
            # Get sentences as list
            sentences = get_sentences_from_text(text)
            # Get summary
            summary_list = get_summary(sentences)

            if not self.summary:
                self.summary = ""
                self.initial_text = ""
                for summary in summary_list:
                    self.summary += summary
                    self.initial_text += summary

            # Get first sentence.
            self.first_sentence = get_first_sentence(sentences)
            if len(self.first_sentence) > 160:
                # https://stackoverflow.com/questions/6266727/python-cut-off-the-last-word-of-a-sentence
                self.first_sentence = self.first_sentence[:160].rsplit(' ', 1)[0]
            elif len(self.first_sentence) < 15:
                self.first_sentence = text[:160]

            # Set publishing date of the document
            self.published_date = timezone.now() + datetime.timedelta(+0)

            # Populating seo related data
            self.seo_title = self.title
            self.seo_description = self.title
            self.seo_description = self.first_sentence
            # self.seo_keywords = ",".join(get_keywords_from_text(text, count=3))

            # Assigning author, sould be 1st superuser
            self.author = get_user_model().objects.filter(is_superuser=True).first()
            # self.subjects.set(get_subjects(text))

            pre, ext = os.path.splitext(filename)
            file_with_pdf_ext = pre + ".pdf"

            temp_dir = tempfile.TemporaryDirectory(prefix=pre)

            # If extension is ppt change document type to presentation
            if ext in ['.ppt', 'pptx']:
                self.type = Document.PRESENTATION

            # convert the uploaded file to pdf file and save it
            os.system('soffice --headless --convert-to pdf --outdir ' + temp_dir.name + ' ' + temp.name)


            # Changing file extension
            # https://stackoverflow.com/questions/2900035/changing-file-extension-in-python
            head, tail = os.path.split(temp.name)
            pre, ext = os.path.splitext(tail)
            pdf_converted_loc = os.path.join(temp_dir.name, pre + ".pdf")

            # Reading generated pdf document from soffice and adding it to our model field
            f = open(pdf_converted_loc, 'rb')
            # myfile = DjangoFile(f)  # Converting to django's File model object
            # self.pdf_converted_file = myfile
            # self.pdf_converted_file.name = file_with_pdf_ext

            # Creating a temp directory where images of pages will be populated.
            images_tmpdir = tempfile.TemporaryDirectory()
            # Converting each page of pdf to images
            pdf_images = convert_from_path(pdf_converted_loc, output_folder=images_tmpdir.name, fmt='jpg', dpi=72) #reduce dpi for converted image

            self.page = pdf_images.__len__()

            self.preview_from = 2
            if self.page <= 1:
                self.preview_from = 1
                self.preview_to = 1
            elif self.page <= 3:
                self.preview_to = 2
            elif self.page <= 5:
                self.preview_to = 3
            elif self.page <= 10:
                self.preview_to = 4
            elif self.page <= 20:
                self.preview_to = 5
            elif self.page <= 30:
                self.preview_to = 7
            elif self.page > 30:
                self.preview_to = 9

            super(Document, self).save(*args, **kwargs)

            # Extracting html of individual pages from pdf file
            page_html_data = get_html_from_pdf_url('file://' + pdf_converted_loc)

            # Creating pages data for document
            page_count = 1
            for pdf_img in pdf_images:
                pdf_images_pre, pdf_images_ext = os.path.splitext(pdf_img.filename)
                page_obj = Page()
                # page_obj.name = pdf_img.filename
                page_obj.no = page_count
                page_obj.image_file = DjangoFile(open(pdf_img.filename, 'rb'), name=uuid.uuid4().hex+pdf_images_ext)
                page_obj.html = page_html_data[page_count]
                page_obj.document = self
                page_obj.author = self.author
                page_obj.save()
                page_count += 1

            # self.cover_image = get_thumbnail(self.pages.first().image_file, '80x112', quality=60, format='PNG',crop='center',).url
            # super(Document, self).save(update_fields=["cover_image"])
            # Adding predicted subjects to document

            for subject in get_subjects(text):
                self.subjects.add(subject)

        else:
            # print("qwertyuioiuytyuiu")
            super(Document, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('documents:document-view', kwargs={'slug': self.slug})


class File(models.Model):
    """Unit of work to be done."""
    key = models.CharField(unique=True, max_length=10, default=key_generator, editable=False)
    file = models.FileField(verbose_name=_('File'), upload_to=all_files, max_length=1000 )
    document = models.ForeignKey(Document, blank=True, null=True, on_delete=models.CASCADE, related_name='document_file')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.key


class Page(models.Model):
    no = models.PositiveIntegerField()
    image_file = models.ImageField(verbose_name=_('Image'), upload_to=images, max_length=1000)
    html = models.TextField(verbose_name=_('Page html'))
    document = models.ForeignKey(Document, blank=True, null=True, on_delete=models.CASCADE, related_name='pages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.document.id

class Issue(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Report(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='report')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    issue = models.ManyToManyField(Issue, related_name='issue', blank=True, null=True)
    other_issue = models.CharField(_('Other Issues'), max_length=2000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document
