import json
from hashlib import sha256

from django.db import models
from django.utils.timezone import now

from django_extensions.db.fields.json import JSONField

from bedrock.contentful.api import contentful


def data_hash(data):
    str_data = json.dumps(data, sort_keys=True)
    return sha256(str_data.encode('utf8')).hexdigest()


class ContentfulEntryManager(models.Manager):
    def get_homepage(self, lang):
        try:
            return self.get(content_type='homepageEn', language=lang).data
        except ContentfulEntry.DoesNotExist:
            return None

    def refresh(self, force=False):
        updated_count = 0
        added_count = 0
        for page in contentful.get_all_page_data():
            hash = data_hash(page)
            try:
                obj = self.get(contentful_id=page['id'])
            except ContentfulEntry.DoesNotExist:
                self.create(
                    contentful_id=page['id'],
                    content_type=page['content_type'],
                    language=page['lang'],
                    data_hash=hash,
                    data=page,
                )
                added_count += 1
            else:
                if force or hash != obj.data_hash:
                    obj.language = page['lang']
                    obj.data_hash = hash
                    obj.data = page
                    obj.save()
                    updated_count += 1

        return added_count, updated_count


class ContentfulEntry(models.Model):
    contentful_id = models.CharField(max_length=20, unique=True)
    content_type = models.CharField(max_length=20)
    language = models.CharField(max_length=5)
    last_modified = models.DateTimeField(default=now)
    data_hash = models.CharField(max_length=64)
    data = JSONField()

    objects = ContentfulEntryManager()

    class Meta:
        unique_together = ('content_type', 'language')
