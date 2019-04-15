from django.db import models

from django_extensions.db.fields.json import JSONField


class NewsletterManager(models.Manager):
    def serialize(self):
        data = {}
        for nl in self.all():
            data[nl.slug] = nl.data
        return data

    def refresh(self, new_data):
        """Update all data in the table from a dict of Newsletter data

        Return None if nothing changed, or number of records otherwise.
        """
        curr_data = self.serialize()
        if new_data == curr_data:
            return None

        self.all().delete()
        count = 0
        for slug, data in new_data.items():
            self.create(
                slug=slug,
                data=data,
            )
            count += 1

        return count


class Newsletter(models.Model):
    slug = models.SlugField(
        unique=True,
        help_text="The ID for the newsletter that will be used by clients",
    )
    data = JSONField()

    objects = NewsletterManager()

    def __unicode__(self):
        return self.slug
