# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.careers.tests import PositionFactory
from bedrock.careers.utils import generate_position_meta_description
from bedrock.mozorg.tests import TestCase


class GeneratePositionMetaDescriptionTests(TestCase):
    def setUp(self):
        self.position = PositionFactory(title="Bowler", position_type="Full time", location="Los Angeles,Ralphs")

    def test_position_type_consonant_beginning(self):
        meta = generate_position_meta_description(self.position)
        self.assertEqual(meta, "Mozilla is hiring a full time Bowler in Los Angeles and Ralphs")

    def test_position_type_vowel_beginning(self):
        self.position.position_type = "intern"
        meta = generate_position_meta_description(self.position)
        self.assertEqual(meta, "Mozilla is hiring an intern Bowler in Los Angeles and Ralphs")

    def test_single_location(self):
        self.position.location = "Los Angeles"
        meta = generate_position_meta_description(self.position)
        self.assertEqual(meta, "Mozilla is hiring a full time Bowler in Los Angeles")

    def test_multiple_locations(self):
        self.position.location = "Los Angeles,Ralphs,In-N-Out"
        meta = generate_position_meta_description(self.position)
        self.assertEqual(meta, "Mozilla is hiring a full time Bowler in In-N-Out, Los Angeles and Ralphs")
