# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.careers.models import Position
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase


class TestPositionModel(TestCase):
    def test_location_list(self):
        PositionFactory(location="San Francisco,Portland")
        pos = Position.objects.get()
        assert pos.location_list == ["Portland", "San Francisco"]

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

    def test_department(self):
        PositionFactory(department="Marketing")
        PositionFactory(department="Engineering")
        PositionFactory(department="Engineering")

        assert Position.categories() == ["Engineering", "Marketing"]
