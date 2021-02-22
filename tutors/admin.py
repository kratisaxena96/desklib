from django.contrib import admin

# Register your models here.
from tutors.models import Tutor, Skills

admin.site.register(Tutor)
admin.site.register(Skills)
