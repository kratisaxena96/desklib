from django.db import models

# Create your models here.
from django.db import models
from subjects.models import Subject


def imguploads(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# declare a new model with a name "Tutor"
class Tutor(models.Model):
    # fields of the model
    profile_pic = models.ImageField(upload_to ='')
    name = models.CharField(max_length=200)
    designation = models.TextField()
    rating = models.IntegerField()
    review_content = models.TextField()
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=60)
    subjects = models.ForeignKey(Subject, db_index=True, blank=True, null=True, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.designation