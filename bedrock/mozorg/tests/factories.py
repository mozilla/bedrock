# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import factory
import wagtail_factories

from bedrock.mozorg import models
from bedrock.mozorg.blocks import leadership


class LeadershipHeadshotBlockFactory(wagtail_factories.StructBlockFactory):
    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    image_alt_text = wagtail_factories.CharBlockFactory
    photos_link = wagtail_factories.CharBlockFactory

    class Meta:
        model = leadership.LeadershipHeadshotBlock


class LeadershipExternalLinkBlockFactory(wagtail_factories.StructBlockFactory):
    url = wagtail_factories.CharBlockFactory
    type = wagtail_factories.CharBlockFactory
    text = wagtail_factories.CharBlockFactory

    class Meta:
        model = leadership.LeadershipExternalLinkBlock


class LeadershipBioBlockFactory(wagtail_factories.StructBlockFactory):
    name = wagtail_factories.CharBlockFactory
    headshot = factory.SubFactory(LeadershipHeadshotBlockFactory)
    job_title = wagtail_factories.CharBlockFactory
    biography = wagtail_factories.CharBlockFactory
    external_links = wagtail_factories.ListBlockFactory(LeadershipExternalLinkBlockFactory)

    class Meta:
        model = leadership.LeadershipBioBlock


class LeadershipGroupBlockFactory(wagtail_factories.StructBlockFactory):
    title = wagtail_factories.CharBlockFactory
    leaders = wagtail_factories.ListBlockFactory(LeadershipBioBlockFactory)

    class Meta:
        model = leadership.LeadershipGroupBlock


class LeadershipSectionBlockFactory(wagtail_factories.StructBlockFactory):
    title = wagtail_factories.CharBlockFactory
    leadership_group = wagtail_factories.ListBlockFactory(LeadershipGroupBlockFactory)

    class Meta:
        model = leadership.LeadershipSectionBlock


class LeadershipPageFactory(wagtail_factories.PageFactory):
    title = "Test Leadership Page"
    live = True
    slug = "leadership"

    leadership_sections = wagtail_factories.StreamFieldFactory({"section": factory.SubFactory(LeadershipSectionBlockFactory)})

    class Meta:
        model = models.LeadershipPage
