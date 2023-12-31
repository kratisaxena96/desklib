# Create your models here.
from django.db import models
from subjects.models import Subject
from django.urls import reverse


def img_uploads(instance, filename):
    return 'tutors/upload/{}'.format(filename)


class Skills(models.Model):
    skill = models.CharField(verbose_name="skill", max_length=50)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill


class Tutor(models.Model):
    slug = models.SlugField(unique=True, max_length=60)
    profile_pic = models.ImageField(verbose_name='profile_pic', upload_to=img_uploads, max_length=500, blank=True)
    name = models.CharField(max_length=200)
    designation = models.CharField(verbose_name="designation", max_length=200)
    rating = models.IntegerField(verbose_name="rating")
    review_count = models.PositiveIntegerField(verbose_name="review_count")
    description = models.TextField()
    price = models.PositiveIntegerField(verbose_name="price")
    subjects = models.ForeignKey(Subject, related_name="subjects", blank=True, null=True, on_delete=models.SET_NULL)
    skills = models.ManyToManyField(Skills, related_name="skills", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation

    def get_absolute_url(self):
        return reverse('tutors:tutor-detail', kwargs={'slug': self.slug})