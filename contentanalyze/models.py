from django.conf import settings
from django.db import models
import os
from django.db.models.fields import CharField, TextField
from uniconGrant.settings import MEDIA_ROOT
from .validators import validate_file

# Create your models here.
# Models for Dictionary


class Author(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Muallif"
        verbose_name_plural = "Mualliflar"

    def __str__(self):
        return self.name


class Soha(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        verbose_name = "Soha"

    def __str__(self):
        return self.name


class Manba(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    fayl = models.FileField(max_length=250, unique=True)
    author = models.ManyToManyField(Author, null=True, blank=True, related_name="manba_mualliflari")
    soha = models.ForeignKey(Soha, on_delete=models.SET_NULL, blank=True, null=True, related_name="soha_to_manba")
    nashr = models.CharField(max_length=100, null=True, blank=True)
    nashrYear = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Manba"

    def __str__(self):
        return self.name


class Lugat(models.Model):
    abbr = models.CharField(max_length=30, blank=True, unique=True, null=True)
    wordLatin = models.CharField(max_length=250, unique=True, blank=True, null=True)
    wordKiril = models.CharField(max_length=250, unique=True, blank=True, null=True)
    wordRus = models.CharField(max_length=250, unique=True, blank=True, null=True)
    wordEnglish = models.CharField(max_length=250, unique=True, blank=True, null=True)
    commentLatin = models.CharField(max_length=500, unique=True, blank=True, null=True)
    commentKiril = models.CharField(max_length=500, unique=True, blank=True, null=True)
    commentRus = models.CharField(max_length=500, unique=True, blank=True, null=True)
    commentEnglish = models.CharField(max_length=500, unique=True, blank=True, null=True)
    soha = models.ForeignKey(Soha, on_delete=models.SET_NULL, blank=True, null=True, related_name="soha_to_lugat")
    manba = models.ForeignKey(Manba, on_delete=models.SET_NULL, blank=True, null=True, related_name="manba_to_lugat")
    muallif = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True, related_name="muallif_to_lugat")

    class Meta:
        verbose_name = "Lugat"
        verbose_name_plural = "Lugatlar"

    def __str__(self):
        return self.wordKiril


# Models for Text Mining


class LugatSoha(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    nameRus = models.CharField(max_length=100, blank=False, unique=True)
    nameEng = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        verbose_name = "lugatSoha"

    def __str__(self):
        return self.name


class Alphabet(models.Model):
    name = models.CharField(max_length=20, blank=False, unique=True)

    class Meta:
        verbose_name = "Alfavit"
        verbose_name_plural = "Alfavit"

    def __str__(self):
        return self.name


class Document(models.Model):
    fayl = models.FileField(max_length=250, unique=True)
    author = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    alphabet = models.ForeignKey(Alphabet, on_delete=models.SET_NULL, null=True, blank=True, related_name="alfavit_to_hujjat")
    sohaID = models.ForeignKey(Soha, on_delete=models.SET_NULL, blank=True, null=True, related_name="soha_to_hujjat")
    nashr = models.CharField(max_length=100, null=True, blank=True)
    nashrYear = models.CharField(max_length=100, null=True, blank=True)
    miningInfo = models.CharField(max_length=250, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjat"

    def __str__(self):
        return self.name

