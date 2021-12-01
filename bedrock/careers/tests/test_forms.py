from bedrock.careers.forms import PositionFilterForm
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase


class PositionFilterFormTests(TestCase):
    def test_dynamic_position_type_choices(self):
        """
        The choices for the position_type field should be dynamically
        generated from the available values in the database.
        """
        PositionFactory.create(position_type="Foo")
        PositionFactory.create(position_type="Bar")
        PositionFactory.create(position_type="Baz")
        PositionFactory.create(position_type="Foo")

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
