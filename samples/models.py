import os
import tempfile
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from documents.models import pdf_converted_files
from django.core.files import File as DjangoFile
from pdf2image import convert_from_path, convert_from_bytes
from documents.models import images




# Create your models here.

def upload_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'sample/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )

class Sample(models.Model):
    RESUME = 1

    TYPE_OF_SAMPLE = (
        (RESUME, 'Resume'),
    )

    name = models.CharField(max_length=250)
    slug = models.SlugField(_('Slug'),unique=True)
    type = models.IntegerField(choices=TYPE_OF_SAMPLE, default=RESUME, db_index=True)
    description = RichTextField(_('Description'), blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='author_samples' )
    upload_sample = models.FileField(verbose_name=_('Upload Sample'), upload_to=upload_to, max_length=1000)
    pdf_converted_file = models.FileField(verbose_name=_(' Pdf converted file'), upload_to=pdf_converted_files, max_length=1000,blank=True, null=True)


    total_downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    search_clicks = models.PositiveIntegerField(default=0)
    google_clicks = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(_('Is Published'), default=True)
    is_visible = models.BooleanField(_('Is Visible'), default=True)

    published_date = models.DateTimeField(_('Published Date'), default=timezone.now)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    seo_title = models.CharField(max_length=70,
                                 help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.')
    seo_description = models.TextField(max_length=160,
                                       help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.')
    seo_keywords = models.CharField(max_length=140,
                                    help_text='Recommended max.length of relevant seo keyword is 140 characters')


    class Meta:
        verbose_name = _('sample')
        verbose_name_plural = _('samples')

    def __str__(self):
        return self.name

    @property
    def sd(self):
        return {
            "@type": 'Sample',
            "description": self.name,
            "name": self.name,
        }



    def get_absolute_url(self):
        return reverse('writing:sample-view', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # Get the complete file path to obtain filename

        # First time save

        self.updated = timezone.now()

        # We only autogenerate data at time of creation.
        if not self.id:
            # Populating created timestamp
            self.created = timezone.now()

            sample_filename = self.upload_sample.name
            sample_filename = os.path.basename(sample_filename)
            sample_filename = sample_filename.replace(' ', '_')

            f1 = self.upload_sample.file  # File to copy from
            temp = tempfile.NamedTemporaryFile(suffix=sample_filename)  # Temporary File to copy to
            # Copying file contents
            with open(temp.name, 'wb') as f2:
                f2.write(f1.read())

            f2.close()

            pre, ext = os.path.splitext(sample_filename)
            file_with_pdf_ext = pre + ".pdf"

            temp_dir = tempfile.TemporaryDirectory(prefix=pre)

            # convert the uploaded file to pdf file and save it
            os.system('soffice --headless --convert-to pdf --outdir ' + temp_dir.name + ' ' + temp.name)

            head, tail = os.path.split(temp.name)
            pre, ext = os.path.splitext(tail)
            pdf_converted_loc = os.path.join(temp_dir.name, pre + ".pdf")

            # Reading generated pdf document from soffice and adding it to our model field
            f = open(pdf_converted_loc, 'rb')
            myfile = DjangoFile(f)  # Converting to django's File model object
            self.pdf_converted_file = myfile
            self.pdf_converted_file.name = file_with_pdf_ext

            # Creating a temp directory where images of pages will be populated.
            images_tmpdir = tempfile.TemporaryDirectory()
            # Converting each page of pdf to images
            pdf_images = convert_from_path(pdf_converted_loc, output_folder=images_tmpdir.name, fmt='jpg')

        super(Sample, self).save(*args, **kwargs)

        # Creating pages data for document
        img_count = 1
        for pdf_img in pdf_images:
            img_obj = Image()
            img_obj.no = img_count
            img_obj.image_file = DjangoFile(open(pdf_img.filename, 'rb'))
            img_obj.sample = self
            img_obj.author = self.author
            img_obj.save()
            img_count += 1




class Image(models.Model):
    no = models.PositiveIntegerField()
    image_file = models.ImageField(verbose_name=_('Image'), upload_to=images, max_length=1000)
    sample = models.ForeignKey(Sample, blank=True, null=True, on_delete=models.CASCADE, related_name='samples')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.document.id













