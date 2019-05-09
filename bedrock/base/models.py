from builtins import object
from django.db import models


class ConfigValue(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    value = models.CharField(max_length=200)

    class Meta(object):
        app_label = 'base'

    def __str__(self):
        return '%s=%s' % (self.name, self.value)


def get_config_dict():
    return {c.name: c.value for c in ConfigValue.objects.all()}
