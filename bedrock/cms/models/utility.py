# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.db import models


class SetAwareEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class SimpleKVStore(models.Model):
    """Allows us to use the DB as a simple key-value store via the ORM"""

    key = models.CharField(
        blank=False,
        max_length=64,
        null=False,
        unique=True,
    )
    value = models.JSONField(
        blank=False,
        null=False,
        encoder=SetAwareEncoder,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<SimpleKVStore entry {self.key}: {self._truncated_display_value}"

    def __str__(self):
        return f"SimpleKVStore entry for {self.key}: {self._truncated_display_value}"

    @property
    def _truncated_display_value(self):
        if len(self.value) > 10:
            return f"{self.value}..."
        else:
            return self.value
