from django.conf import settings
from django.db import models


class ArticleImage(models.Model):
    original = models.CharField(max_length=2000)
    name = models.CharField(max_length=2000)
    alt = models.CharField(max_length=2000, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return settings.OPENSTANDARD_IMAGE_URL + self.name


class Article(models.Model):
    author = models.CharField(max_length=2000)
    category = models.CharField(max_length=255)
    image = models.ForeignKey(ArticleImage, blank=True, null=True)
    link = models.CharField(max_length=2000)
    title = models.CharField(max_length=2000)
    summary = models.CharField(max_length=2000)
    published = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link
