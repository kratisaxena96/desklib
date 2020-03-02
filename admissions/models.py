from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import datetime


def upload_to(instance, filename):
    now = timezone.now()

    return 'admissions/{}/{}'.format(
        now.strftime("%Y/%m/%d/"),
        filename,
    )


# class Country(models.Model):
#     COUNTRY_CHOICES = [
#         ('US', 'US'),
#         ('RO', 'Romania'),
#     ]
#     # name
#     country_code = models.CharField(max_length=30, choices=COUNTRY_CHOICES)
#     # flag
#     # icon
#
#     def __str__(self):
#         return str(self.country_code)
#
#
# class Courses(models.Model):
#     course = models.CharField(max_length=50)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_courses',
#                                 verbose_name=_('Country'))
#
#     def __str__(self):
#         return str(self.course)


class AspirantDetails(models.Model):
    """
    Model to take details of aspirants for admissions
    """

    QUALIFICATION = (
        ('under_grad', 'Under Graduate'),
        ('graduate', 'Graduate'),
        ('post_graduate', 'Post Graduate'),
        ('doctorate', 'Doctorate'),
    )
    STREAM = (
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('tech', 'Technology'),
        ('commerce', 'Commerce')
    )
    COUNTRY = (
        ('uk', 'United Kingdom'),
        ('australia', 'Australia'),
    )
    COURSES = (
        ('accounts','Accounting & Finance'),
        ('aeronautics','Aeronautical & Manufacturing Engineering'),
        ('agriculture','Agriculture & Forestry'),
        ('american','American Studies'),
        ('physiology','Anatomy & Physiology'),
        ('anthropology','Anthropology'),
        ('architecture','Architecture'),
        ('arts','Art & Design')
    )
    country = models.CharField(_('Country'), max_length=70, choices=COUNTRY)
    name = models.CharField(_('Name'), max_length=70)
    email = models.EmailField(_('Email'), max_length=255)
    phone = PhoneNumberField(_('Phone No'), null=False, blank=False, unique=True)
    qualification = models.CharField(_('Qualification'),max_length=30, choices=QUALIFICATION)
    stream = models.CharField(_('Stream'),max_length=30, choices=STREAM)
    resume = models.FileField(_('Upload Resume'), upload_to=upload_to, max_length=1000)
    lokking_for_stream = models.CharField(_('Looking For Stream'),max_length=30, choices=STREAM)
    lokking_for_course = models.CharField(_('Looking for Course'), max_length=70, choices=COURSES)
    year = models.IntegerField(_('Session Year'), max_length=6,)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Aspirant Detail')
        verbose_name_plural = _('Aspirant Details')
