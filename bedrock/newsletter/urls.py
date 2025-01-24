# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.urls import path

from bedrock.utils.views import VariationTemplateView

urlpatterns = (
    path(
        "newsletter/",
        VariationTemplateView.as_view(
            template_name="newsletter/index.html", template_context_variations=["1", "2"], ftl_files=["mozorg/newsletters"]
        ),
        name="newsletter",
    ),
)
