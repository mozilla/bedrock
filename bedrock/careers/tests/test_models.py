# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.cache import cache
from django.db.backends.base.operations import BaseDatabaseOperations

from bedrock.careers.models import Position
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase


class TestPositionModel(TestCase):
    def setUp(self):
        cache.clear()

    def test_location_list(self):
        PositionFactory(location="San Francisco,Portland")
        pos = Position.objects.get()
        assert pos.location_list == ["Portland", "San Francisco"]

    def test_location_list_splits_on_semicolons(self):
        PositionFactory(location="Remote Belgium; Remote Denmark; Remote Finland")
        pos = Position.objects.get()
        assert pos.location_list == ["Remote Belgium", "Remote Denmark", "Remote Finland"]

    def test_location_list_is_per_position(self):
        PositionFactory(id=1, location="Toronto")
        PositionFactory(id=2, location="Berlin,Paris")

        assert Position.objects.get(id=2).location_list == ["Berlin", "Paris"]
        assert Position.objects.get(id=1).location_list == ["Toronto"]

    def test_cover(self):
        PositionFactory(id=1, title="Job", job_locations="Remote US", internal_job_id=999)
        PositionFactory(id=2, title="Cover", job_locations="Remote", internal_job_id=999)

        pos = Position.objects.get(id=1)
        cover = pos.cover
        assert cover.id == 2
        assert cover.title == "Cover"
        assert cover.job_locations == "Remote"

    def test_position_types(self):
        PositionFactory(position_type="Full time")
        PositionFactory(position_type="Part time")
        PositionFactory(position_type="Part time")

        assert Position.position_types() == ["Full time", "Part time"]

    def test_locations(self):
        PositionFactory(job_locations="Remote US,Remote CA")
        PositionFactory(job_locations="Remote CA,San Francisco")
        PositionFactory(job_locations="Remote")  # The "cover" should be excluded.

        assert Position.locations() == ["Remote CA", "Remote US", "San Francisco"]

    def test_locations_splits_on_semicolons(self):
        PositionFactory(job_locations="Remote Belgium;Remote Denmark")
        PositionFactory(job_locations="Remote France;Remote Netherlands")
        PositionFactory(job_locations="Remote")

        assert Position.locations() == ["Remote Belgium", "Remote Denmark", "Remote France", "Remote Netherlands"]

    def test_department(self):
        PositionFactory(department="Marketing")
        PositionFactory(department="Engineering")
        PositionFactory(department="Engineering")

        assert Position.categories() == ["Engineering", "Marketing"]

    def test_is_moco_false_for_mofo_jobs(self):
        assert PositionFactory(department="Engineering").is_moco
        assert not PositionFactory(department="Engineering", is_mofo=True).is_moco
        assert not PositionFactory(department="Mozilla Foundation").is_moco

    def test_employer(self):
        assert PositionFactory(department="Engineering").employer == "Mozilla Corporation"
        assert PositionFactory(department="Grantmaking", is_mofo=True).employer == "Mozilla Foundation"
        assert PositionFactory(department="MZLA/Thunderbird").employer == "MZLA/Thunderbird"

    def test_internal_job_id_column_fits_newer_greenhouse_ids(self):
        # Newer Greenhouse tenants (e.g. the mozillafoundation board) issue ids
        # above 2**31, which overflow a 32-bit integer column on PostgreSQL.
        # SQLite stores every integer as 64 bits, so the test database cannot
        # catch this; check the field type's standard range instead.
        field = Position._meta.get_field("internal_job_id")
        low, high = BaseDatabaseOperations.integer_field_ranges[field.get_internal_type()]
        assert low <= 4_141_464_005 <= high
