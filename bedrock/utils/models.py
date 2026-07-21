# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from django.db import models

import timeago


class GitRepoState(models.Model):
    repo_name = models.CharField(max_length=200, blank=True)
    repo_url = models.CharField(max_length=200, blank=True)
    repo_id = models.CharField(max_length=100, db_index=True, unique=True)
    latest_ref = models.CharField(max_length=100)
    latest_ref_timestamp = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.repo_name}: {self.latest_ref}"

    @property
    def commit_url(self):
        if self.repo_url:
            return f"{self.repo_url}/commit/{self.latest_ref}"

        return ""

    @property
    def is_private(self):
        # Heuristic: Mozilla suffixes private repo names with "-private", and
        # `clean_remote_url` strips `.git` and trailing slashes before we store
        # the URL, so an endswith match is reliable for the current callers.
        return self.repo_url.endswith("-private") if self.repo_url else False

    @property
    def last_updated(self):
        if self.latest_ref_timestamp:
            latest_datetime = datetime.fromtimestamp(self.latest_ref_timestamp)
            return timeago.format(latest_datetime)

        return "unknown"
