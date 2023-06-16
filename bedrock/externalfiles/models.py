# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models


class ExternalFile(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "externalfiles"

    def __str__(self):
        return f"{self.name}"
