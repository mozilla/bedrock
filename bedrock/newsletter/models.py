from django.db import models

from django_extensions.db.fields.json import JSONField


class Newsletter(models.Model):
    slug = models.SlugField(
        unique=True,
        help_text="The ID for the newsletter that will be used by clients",
    )
    data = JSONField()
