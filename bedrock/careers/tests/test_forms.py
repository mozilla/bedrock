# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.careers.forms import PositionFilterForm
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase


class PositionFilterFormTests(TestCase):
    def test_dynamic_position_type_choices(self):
        """
        The choices for the position_type field should be dynamically
        generated from the available values in the database.
        """
        PositionFactory(position_type="Foo")
        PositionFactory(position_type="Bar")
        PositionFactory(position_type="Baz")
        PositionFactory(position_type="Foo")
        PositionFactory(position_type="")

        form = PositionFilterForm()
        self.assertEqual(
            form.fields["position_type"].choices,
            [
                ("", "All Positions"),
                ("Bar", "Bar"),  # Alphabetical order
                ("Baz", "Baz"),
                ("Foo", "Foo"),
            ],
        )

    def test_locations(self):
        """
        Test locations, and that "All Offices" and an errant empty value is not
        included, and the choices are sorted.
        """
        PositionFactory(job_locations="All Offices,,Mountain View,Canada")

        form = PositionFilterForm()
        self.assertEqual(
            form.fields["location"].choices,
            [
                ("", "All Locations"),
                ("Canada", "Canada"),
                ("Mountain View", "Mountain View"),
            ],
        )

    def test_categories(self):
        """
        Test categories, and an errant empty value is not included, and the
        choices are sorted.
        """
        PositionFactory(department="Marketing")
        PositionFactory(department="")
        PositionFactory(department="IT")

        form = PositionFilterForm()
        self.assertEqual(
            form.fields["team"].choices,
            [
                ("", "All Teams"),
                ("IT", "IT"),
                ("Marketing", "Marketing"),
            ],
        )
