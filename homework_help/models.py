import os
import random
import string
import tempfile
import uuid
import itertools

import textract
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from subjects.models import Subject
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.template.defaultfilters import truncatechars
from meta.models import ModelMeta
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site


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
    # filename_base, filename_ext = os.path.splitext(instance.title)
    # uid = instance.content_object.uuid

    return 'homework_help/question/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        instance.title
    )


def upload_answer_to(instance, filename):
    now = timezone.now()
    # now = timezone.localtime(timezone.now())
    # filename_base, filename_ext = os.path.splitext(filename)
    # uid = instance.content_object.uuid

    return 'homework_help/answer/{}/{}'.format(
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


class Question(ModelMeta, models.Model):
    question = models.TextField(_('Question'))
    slug = models.SlugField(_('Slug'), unique=True, max_length= 200)
    # upload_file = models.FileField(verbose_name=_('Upload File'), upload_to=upload_to, max_length=1000)
    subjects = models.ForeignKey(Subject, db_index=True, blank=True, null=True, related_name='subject_question',
                                 on_delete=models.PROTECT, )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='author_question')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_published = models.BooleanField(_('Is Published'), default=False)
    is_visible = models.BooleanField(_('Is Visible'), default=False)

    published_date = models.DateTimeField(_('Published Date'), default=timezone.now)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seo_title = models.CharField(max_length=90,
                                 help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.', null=True, blank=True)
    seo_description = models.TextField(max_length=160,
                                       help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.', null=True, blank=True)
    seo_keywords = models.CharField(max_length=140,
                                    help_text='Recommended max.length of relevant seo keyword is 140 characters', null=True, blank=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('homework_help:question-detail-view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.question
        # self.slug = slugify(truncatechars(value, 50))
        # super(Question, self).save(*args, **kwargs)
        # self.slug = slugify(truncatechars(value, 50)+str(self.pk))
        if not self.id:
            slug_question = slug_original = slugify(truncatechars(value, 50))

            for i in itertools.count(1):
                if not Question.objects.filter(slug=slug_question).exists():
                    break
                slug_question = '{}-{}'.format(slug_original, i)

            self.slug = slug_question
            self.seo_title = truncatechars(value, 50)
            self.seo_description = value
        super().save(*args, **kwargs)


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

    # @property
    # def sd(self):
    #     return {
    #         "@type": 'Document',
    #         "description": self.seo_description,
    #         "name": self.seo_title,
    #     }


class QuestionFile(models.Model):
    """
    File attached to a Question.
    """

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField(_('title'), max_length=500, null=True, blank=True)
    # slug = models.SlugField(prepopulate_from=("title",))
    file = models.FileField(verbose_name=_('Question File'), upload_to=upload_question_to, max_length=1000)
    question = models.ForeignKey(Question, related_name='user_questionfiles', on_delete=models.CASCADE, null=True, blank=True)
    require_recalculation = models.BooleanField(_('Require Recalculation'), default=False)
    # visible = models.BooleanField(default=True)
    content = models.TextField(_('content'), null=True, blank=True)
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

            # self.title = self.file.name

            filename = self.file.name
            filename = os.path.basename(filename)
            filename = filename.replace(' ', '_')
            f1 = self.file.file
            temp = tempfile.NamedTemporaryFile(suffix=filename)
            with open(temp.name, 'wb') as f2:
                f2.write(f1.read())
            f2.close()
            self.content = textract.process(temp.name).decode("utf-8")


            filename_base, filename_ext = os.path.splitext(self.file.name)
            self.title = str(uuid.uuid4()) + filename_ext

        self.updated = timezone.now()
        if self.require_recalculation:
            filename = self.file.name
            filename = os.path.basename(filename)
            filename = filename.replace(' ', '_')
            f1 = self.file.file
            temp = tempfile.NamedTemporaryFile(suffix=filename)
            with open(temp.name, 'wb') as f2:
                f2.write(f1.read())
            f2.close()
            self.content = textract.process(temp.name).decode("utf-8")
        return super(QuestionFile, self).save(*args, **kwargs)


class Order(ModelMeta, models.Model):
    STATUS_RECIEVED = 1
    STATUS_PAYMENT_UPDATED = 2
    STATUS_EXPERT_WORKING = 3
    STATUS_ANSWER_POSTED = 4

    STATUS = [
        (STATUS_RECIEVED, 'Question Recieved'),
        (STATUS_PAYMENT_UPDATED, 'Payment Updated'),
        (STATUS_EXPERT_WORKING, 'Expert Working on your Answer'),
        (STATUS_ANSWER_POSTED, 'Answer is posted'),
    ]

    question = models.ForeignKey(Question, related_name='ordered_question', on_delete=models.PROTECT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='user_order')
    status = models.IntegerField(choices=STATUS, default=STATUS_RECIEVED, db_index=True)
    remarks = models.TextField(_('Remarks'), null=True, blank=True)
    budget = models.IntegerField(_('Budget'), null=True, blank=True)
    amount_paid = models.IntegerField(_('Amount Paid'), default=0, null=True, blank=True)
    order_id = models.CharField(unique=True, max_length=10, default=key_generator, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_timezone = models.CharField(_('Client TimeZone'),max_length=200, blank=True, null=True)
    expected_hours = models.IntegerField(_('Expected Time'), null=True, blank=True)
    deadline_datetime = models.DateTimeField(_('Deadline Time'), blank=True, null=True)

    is_accepted = models.BooleanField(_('Is Accepted'), default=False)
    is_detailed = models.BooleanField(_('Is Detailed'), default=False)
    is_paid = models.BooleanField(_('Is Paid'), default=False)

    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse('homework_help:order-detail-view', kwargs={'uuid': self.uuid})

    _metadata = {
            'use_og': 'True',
            'use_facebook': 'True',
            'use_twitter': 'True',
            'use_title_tag': 'False',
            'use_googleplus': 'True',
            'use_sites': 'True',
            # 'keywords': 'seo_keywords',
            'title': 'order_id',
            # 'description': 'seo_description',
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

    def save(self, *args, **kwargs):
        value = self.budget
        # self.slug = slugify(truncatechars(value, 50))
        # super(Question, self).save(*args, **kwargs)
        # self.slug = slugify(truncatechars(value, 50)+str(self.pk))
        ip = "https://" + Site.objects.get_current().domain
        if value and self.status == 2:

            locus_email = "kushagra.goel@locusrags.com"
            if not settings.DEBUG:
                locus_email = "info@desklib.com"

            subject = 'Budget for ' + self.order_id + '... updated'
            message = 'Budget for ' + self.order_id + '... updated'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.author.email],
            contex = {'first_name': self.author.first_name, 'order_id': self.order_id, 'budget': self.budget,
                      'SITE_URL': ip, 'uuid': self.uuid }
            htmly = render_to_string('homework_help/mail-templates/budget_for_order_added.html',
                                     context=contex, request=None)
            html_message = htmly
            # html_message = "Hello " + self.author.first_name + ",<br>Budget for your order " + self.order_id + " has been updated. Your budget is " + str(self.budget) + ".<br><a href=" + ip + reverse('homework_help:order-detail-view', kwargs={'uuid': self.uuid}) + "> click here to check budget.</a> "
            mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)

            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)

        if self.status == 4:

            subject = 'Answer for ' + self.order_id + '... updated'
            message = 'Answer for ' + self.order_id + '... updated'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.author.email],
            contex = {'first_name': self.author.first_name, 'order_id': self.order_id,
                      'SITE_URL': ip, 'uuid': self.uuid }
            htmly = render_to_string('homework_help/mail-templates/answer_for_order_added.html',
                                     context=contex, request=None)
            html_message = htmly
            # html_message = "Hello " + self.author.first_name + ",<br>Answer for your order " + self.order_id + " has been updated.<br><a href=" + ip + reverse('homework_help:order-detail-view', kwargs={'uuid': self.uuid}) + "> click here to check answer.</a> "
            mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)

            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)

        super().save(*args, **kwargs)


class Answers(models.Model):
    question = models.ForeignKey(Question, related_name='answer_question', on_delete=models.PROTECT)
    solution = models.TextField(_('Solution'))
    # solution_files = models.FileField(verbose_name=_('Upload File'), upload_to=upload_solutions, max_length=1000)
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


class AnswerFile(models.Model):
    """
    File attached to a Answer.
    """

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField(_('title'), max_length=500, null=True, blank=True)
    # slug = models.SlugField(prepopulate_from=("title",))
    file = models.FileField(verbose_name=_('Answer File'), upload_to=upload_answer_to, max_length=1000)
    answer = models.ForeignKey(Answers, related_name='user_answerfiles', on_delete=models.CASCADE)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return os.path.join(settings.MEDIA_URL,  self.file.url)
        return self.file.url

    def save(self, *args, **kwargs):
        # ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        self.title = self.file.name
        return super(AnswerFile, self).save(*args, **kwargs)



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


