# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

from bedrock.careers.models import Position


class PositionFilterForm(forms.Form):
    team = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off"}))
    position_type = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off"}))
    location = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off"}))

    def __init__(self, *args, **kwargs):
        super(PositionFilterForm, self).__init__(*args, **kwargs)

        # Populate position type choices dynamically.
        locations = Position.locations()
        if "All Offices" in locations:
            locations.remove("All Offices")
        if "" in locations:
            locations.remove("")

        self.fields["location"].choices = [("", "All Locations")] + [(loc, loc) for loc in locations]

        types = Position.position_types()
        if "" in types:
            types.remove("")

        self.fields["position_type"].choices = [("", "All Positions")] + [(typ, typ) for typ in types]

        categories = Position.categories()
        if "" in categories:
            categories.remove("")

        self.fields["team"].choices = [("", "All Teams")] + [(kat, kat) for kat in categories]
