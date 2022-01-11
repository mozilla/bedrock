# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models


class ConfigValue(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    value = models.CharField(max_length=200)

    class Meta:
        app_label = "base"

    def __str__(self):
        return f"{self.name}={self.value}"


def get_config_dict():
    return {c.name: c.value for c in ConfigValue.objects.all()}
