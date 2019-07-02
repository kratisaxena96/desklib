from django.db import models

class Compare(models.Model):
    textarea1 = models.CharField(max_length=10000, blank=True, null=True)
    textarea2 = models.CharField(max_length=10000, blank=True, null=True)


class Spell(models.Model):
    spell_textarea = models.CharField(max_length=10000, blank=True, null=True)