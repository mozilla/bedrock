# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms


class SendToDeviceWidgetForm(forms.Form):
    email = forms.EmailField(max_length=100, required=False)
    platform = forms.ChoiceField(
        choices=(
            ("ios", "ios"),
            ("android", "android"),
            ("all", "all"),
        ),
        required=False,
    )
