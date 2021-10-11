from django.db import models
from django.utils.timezone import now
from django_extensions.db.fields.json import JSONField


class ContentfulEntryManager(models.Manager):
    def get_page_by_id(self, content_id):
        return self.get(contentful_id=content_id).data

    def get_page(self, content_type, lang):
        return self.get(content_type=content_type, language=lang).data

    def get_homepage(self, lang):
        return self.get(content_type="connectHomepage", language=lang).data


class ContentfulEntry(models.Model):
    contentful_id = models.CharField(max_length=20, unique=True)
    content_type = models.CharField(max_length=20)
    language = models.CharField(max_length=5)
    last_modified = models.DateTimeField(default=now)
    url_base = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    data_hash = models.CharField(max_length=64)
    data = JSONField()

    objects = ContentfulEntryManager()
