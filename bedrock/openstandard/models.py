from django.conf import settings
from django.db import models


class ArticleImage(models.Model):
    original = models.CharField(max_length=2000)
    local_path = models.CharField(max_length=2000)
    alt = models.CharField(max_length=2000, blank=True)

    def get_absolute_url(self):
        return settings.MEDIA_URL + self.local_path


class Article(models.Model):
    category = models.CharField(max_length=255)
    image = models.ForeignKey(ArticleImage, blank=True, null=True)
    link = models.CharField(max_length=2000)
    summary = models.CharField(max_length=2000)

    def get_absolute_url(self):
        return self.link
