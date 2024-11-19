# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories
from wagtail import models as wagtail_models

from bedrock.cms import models


class WagtailUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ("username",)

    email = "testuser@example.com"
    password = factory.PostGenerationMethodCall("set_password", "te5tus3r")
    username = "testuser"

    is_superuser = False
    is_staff = True
    is_active = True


class SimpleRichTextPageFactory(wagtail_factories.PageFactory):
    title = "Test SimpleRichTextPage"
    live = True
    slug = "homepage"

    class Meta:
        model = models.SimpleRichTextPage


class LocaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtail_models.Locale


class StructuralPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.StructuralPage
