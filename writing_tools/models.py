from django.db import models

# Create your models here.

class Compare(models.Model):
    textarea1 = models.CharField(max_length=1000, blank=True, null=True)
    textarea2 = models.CharField(max_length=1000, blank=True, null=True)


class Spell(models.Model):
    spell_textarea = models.CharField(max_length=1000, blank=True, null=True)