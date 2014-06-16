from django.db import models

from picklefield import PickledObjectField
from django_extensions.db.fields import ModificationDateTimeField


class TwitterCache(models.Model):
    account = models.CharField(max_length=100, db_index=True, unique=True)
    tweets = PickledObjectField(default=list)
    updated = ModificationDateTimeField()
