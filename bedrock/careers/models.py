# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from itertools import chain

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.urls import reverse


class Position(models.Model):
    job_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
    job_locations = models.CharField(max_length=500, default="")
    # TODO remove this as there is more than just mofo
    is_mofo = models.BooleanField(default=False)
    description = models.TextField()
    apply_url = models.URLField()
    source = models.CharField(max_length=100)
    position_type = models.CharField(max_length=100)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    # Store the Greenhouse internal ID for grouping the same jobs with multiple
    # listings per location.
    internal_job_id = models.PositiveIntegerField()

    NON_MOCO_DEPTS = [
        "Pan Mozilla",
        "Mozilla Foundation",
        "MZLA/Thunderbird",
    ]

    class Meta:
        ordering = (
            "department",
            "title",
        )

    def __str__(self):
        return f"{self.job_id}@{self.source}"

    def get_absolute_url(self):
        return reverse("careers.position", kwargs={"source": self.source, "job_id": self.job_id})

    @classmethod
    def _get_cache_key(cls, name):
        return f"careers_position__{name}"

    @property
    def is_moco(self):
        return self.department not in self.NON_MOCO_DEPTS

    @property
    def location_list(self):
        _key = self._get_cache_key("location_list")
        location_list = cache.get(_key)
        if location_list is None:
            location_list = sorted(self.location.split(","))
            cache.set(_key, location_list, settings.CACHE_TIME_LONG)
        return location_list

    @classmethod
    def position_types(cls):
        _key = cls._get_cache_key("position_types")
        position_types = cache.get(_key)
        if position_types is None:
            position_types = sorted(set(cls.objects.values_list("position_type", flat=True)))
            cache.set(_key, position_types, settings.CACHE_TIME_LONG)
        return position_types

    @classmethod
    def locations(cls):
        _key = cls._get_cache_key("locations")
        locations = cache.get(_key)
        if locations is None:
            locations = sorted(
                {
                    location.strip()
                    for location in chain(
                        *[locations.split(",") for locations in cls.objects.exclude(job_locations="Remote").values_list("job_locations", flat=True)]
                    )
                }
            )
            cache.set(_key, locations, settings.CACHE_TIME_LONG)
        return locations

    @classmethod
    def categories(cls):
        _key = cls._get_cache_key("categories")
        categories = cache.get(_key)
        if categories is None:
            categories = sorted(set(cls.objects.values_list("department", flat=True)))
            cache.set(_key, categories, settings.CACHE_TIME_LONG)
        return categories

    @property
    def cover(self):
        # Try to get the job posting of the same `internal_job_id` with "Remote"
        # job location to use as the "cover" posting.
        if cover := Position.objects.filter(internal_job_id=self.internal_job_id, job_locations="Remote").first():
            return cover

        # Fallback to returning `self` if there is no "Remote" location.
        return self
