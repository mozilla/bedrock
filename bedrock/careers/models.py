# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from itertools import chain

from django.db import models
from django.urls import reverse


class Position(models.Model):
    job_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
    job_locations = models.CharField(max_length=500, default="")
    is_mofo = models.BooleanField(default=False)
    description = models.TextField()
    apply_url = models.URLField()
    source = models.CharField(max_length=100)
    position_type = models.CharField(max_length=100)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    # Store the Greenhouse internal ID for grouping the same jobs with multiple
    # listings per location.
    internal_job_id = models.PositiveIntegerField()

    class Meta:
        ordering = (
            "department",
            "title",
        )

    def __str__(self):
        return f"{self.job_id}@{self.source}"

    @property
    def location_list(self):
        return sorted(self.location.split(","))

    def get_absolute_url(self):
        return reverse("careers.position", kwargs={"source": self.source, "job_id": self.job_id})

    @classmethod
    def position_types(cls):
        return sorted(set(cls.objects.values_list("position_type", flat=True)))

    @classmethod
    def locations(cls):
        return sorted(
            {location.strip() for location in chain(*[locations.split(",") for locations in cls.objects.values_list("location", flat=True)])}
        )

    @classmethod
    def categories(cls):
        return sorted(set(cls.objects.values_list("department", flat=True)))
